
from django.conf.urls import url
from django.views import generic
from django.template import Context
from dal import autocomplete
from .models import Tag
from .forms import TForm

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.custom_login, name='custom_login'),
    url(r'^logout/$', views.custom_logout, name='custom_logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^home/$', views.UpdateView.as_view(), name='test_view'),
    url(r'^search/$', views.search, name='search'),
    url(r'^question/(?P<question_id>[0-9]+)/$', views.question_answer_view, name='question_answer_view'),
    url(r'^add-answer/(?P<question_id>[0-9]+)/$', views.add_answer, name='add_answer'),
    url(r'^add-question/$', views.add_question, name='add_question'),
    url(r'^ajax/upvote/$', views.upvote, name='upvote'),
    url(r'^ajax/downvote/$', views.downvote, name='downvote'),
    url(r'^ajax/accept_solution/$', views.accept_solution, name='accept_solution'),
    url(r'^ajax/check_spam/$', views.check_spam, name='check_spam'),
    url('test-autocomplete/$', autocomplete.Select2QuerySetView.as_view(model=Tag, create_field='name',), name='select2_many_to_many_autocomplete'),
    url(r'^profile/(?P<citrix_user_id>[0-9]+)/$', views.userprofile, name='userprofile'),
]
