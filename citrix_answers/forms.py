from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from citrix_answers.models import Employee, Question
from dal import autocomplete

class SignUpForm(UserCreationForm):
    designation = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'whatclass'}))
    team = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'whatclass'}))
	
    password1 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'class': 'whatclass'}), label="Password")
    password2 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'class': 'whatclass'}), label="Confirm Password")
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5, 'class': 'whatclass'}))

    class Meta:
        model = User
        widgets = {
            'username': forms.TextInput(attrs={'class': 'whatclass'}),
			}
        fields = ('username','password1', 'password2','designation', 'team', 'description',  )


class TForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('tags',)
        widgets = {
            'tags': autocomplete.ModelSelect2Multiple(
                'select2_many_to_many_autocomplete'
            )
        }