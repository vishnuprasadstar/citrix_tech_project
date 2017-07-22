from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from citrix_answers.models import Question, Answer, Tag, Employee
from django.template import context
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from django.views import generic
from django.urls import reverse_lazy

import spam

import operator
from citrix_answers.forms import SignUpForm, TForm

# Create your views here.
def custom_login(request):
	user = authenticate(username=request.POST['username'], password=request.POST['password'])
	if user is not None:
                login(request, user)
		return HttpResponseRedirect('/home/')
		#return HttpResponse("Logged in")
	else:
		return HttpResponse("Cannot find user")


def custom_logout(request):
        logout(request)
	return HttpResponseRedirect('/')

def home(request):
	context = {}
	return render(request, 'homepage.html',context)

class UpdateView(generic.UpdateView):
    model = Tag
    form_class = TForm
    template_name = 'questions_list.html'

    def get(self, request):
	if request.user.is_authenticated():
	    form = self.form_class(initial=self.initial)
            all_questions = Question.objects.all().order_by('-views')
            unanswered_questions = Question.objects.filter(question_answer=None)
            all_tags = Tag.objects.all()
            context = {
                    'question_list': all_questions,
                    'unanswered_question_list': unanswered_questions,
                    'tag_list': all_tags,
					'tag_form' : form,
            }
            return render(request, 'questions_list.html', context)
        else:
            return HttpResponse("User is not logged in....!")

    def get_object(self):
        return Tag.objects.first()


def home(request):
	context = {}
	return render(request, 'homepage.html',context)

def question_answer_view(request, question_id):
    question = Question.objects.get(pk=question_id)
    question_tags = list(question.tags.all())
    if len(question_tags) == 0:
            tag_related_question = []
    else:
            tag_related_question = list(Question.objects.filter(reduce(operator.or_, (Q(tags__name__iexact = x) for x in question_tags))).order_by('updated_at'))
            tag_related_question.remove(question)
    question.views = question.views+1
    question.save()
    answers = list(Answer.objects.filter(question=question).order_by('-upvotes'))
    accepted_answer = list(Answer.objects.filter(question=question).filter(is_solution=1))

    if len(accepted_answer) == 1:
            answers.remove(accepted_answer[0])
    accepted_answer.extend(answers)
    context = {
            'answer_list': accepted_answer,
            'question': question,
            'tag_related_question': tag_related_question,
    }
    return render(request, 'question_answer.html', context)

def add_answer(request, question_id):
    question = Question.objects.get(pk=question_id)
    answer = Answer(
        content=request.POST['new_answer'],
        question=question,
        user=request.user
    )
    answer.save()
    emp = Employee.objects.get(user = request.user)
    emp.rating += 5
    emp.save()
    return redirect('/question/'+str(question.pk))
    #return HttpResponse("Answer added successfully")

def add_question(request):
        question_content = request.POST['new_question_title']
        question = Question(
                title=request.POST['new_question_title'],
                description=request.POST['new_question_description'],
                user=request.user
        )

        question.save()
        emp = Employee.objects.get(user = request.user)
        emp.rating += 2
        emp.save()
        question_id = question.pk;

        question_tags_str = request.POST.getlist('tags')
        for tag in question_tags_str:
                try:
                        tag_object = Tag.objects.get(pk=tag)
                except:
                        tag_object = Tag(tag_name=tag)
                        tag_object.save()

                question.tags.add(tag_object)
        return redirect('/question/'+str(question_id))
        #return HttpResponse("Question added successfully")

def upvote(request):
        #import ipdb; ipdb.set_trace()
        answer_id = int(request.GET['answer_id'][:-8])
        answer = Answer.objects.get(pk=answer_id)
        answer.upvotes = answer.upvotes+1
        answer.save()
        emp = Employee.objects.get(user=answer.user)
        emp.rating += 2
        emp.save()
        emp = Employee.objects.get(user = request.user)
        emp.rating += 1
        emp.save()
        return JsonResponse({'upvotes': answer.upvotes})

def downvote(request):
        #import ipdb; ipdb.set_trace()
        answer_id = int(request.GET['answer_id'][:-10])
        answer = Answer.objects.get(pk=answer_id)
        answer.downvotes = answer.downvotes+1
        answer.save()
        emp = Employee.objects.get(user = answer.user)
        emp.rating -= 1
        emp.save()
        emp = Employee.objects.get(user = request.user)
        emp.rating -= 1
        emp.save()
        return JsonResponse({'downvotes': answer.downvotes})

def search(request):
	idseq = request.POST['search_term'].split()
	tag_search = request.POST['search_term'].startswith("#")

	if(tag_search):
		tag = request.POST['search_term'].split()
		if(len(tag) > 1):
			result = Question.objects.filter(reduce(operator.or_, (Q(tags__name__iexact = x[1:]) for x in tag))).order_by('updated_at')
		else:
			result = Question.objects.filter(tags__name__iexact = tag[0][1:])
	else:
		result = Question.objects.filter(Q(title__icontains = idseq)|reduce(operator.or_, (Q(title__icontains = x) for x in idseq))).order_by('updated_at')

	context = {'search_question_list' : result}
	return render(request, 'search_questions_list.html', context)

def accept_solution(request):
        answer_id = int(request.GET['answer_id'][:-16])
        answer = Answer.objects.get(pk=answer_id)

        q = answer.question
        q.has_solution = 1
        q.save()
        emp = Employee.objects.get(user = answer.user)
        emp.rating += 10
        emp.save()
        emp = Employee.objects.get(user = request.user)
        emp.rating += 3
        emp.save()

        answer.is_solution = 1
        answer.save()
        return JsonResponse({'result': 'success'})

def check_spam(request):
        text = request.GET['title_text']
        filename = 'citrix_answers/data/Data.csv'
	spam.load(filename)
	prob = spam.query(text)
        if prob > 0.5:
                return JsonResponse({'spam': 'True'})
        else:
                return JsonResponse({'spam': 'False'})

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			employee = Employee(
				citrix_username=request.POST['username'],
				description=request.POST['description'],
				designation=request.POST['designation'],
				team=request.POST['team'],
				user=user
			)
			employee.save()
			return redirect('test_view')
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})

def userprofile(request, citrix_user_id):
	employee = Employee.objects.get(user__pk=citrix_user_id)
	answers = list(Answer.objects.filter(user__pk=citrix_user_id))
	accepted_answers = list(Answer.objects.filter(user__pk=citrix_user_id).filter(is_solution=1))
	questions = list(Question.objects.filter(user__pk=citrix_user_id))
	context = {
	    'employee' :employee,
		'accepted_answers_list': accepted_answers,
		'answers_list': answers,
		'questions_list': questions
	}
	return render(request, 'profile.html', context)
