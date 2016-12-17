from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import IbkUser


class IbkUserSignUpForm(ModelForm):
	password2 = forms.CharField(label=_("Confirm Password"),widget=forms.PasswordInput(attrs={ 'type': 'password','id': 'confirm_signup_password', 'name': 'confirm_signup_password','required': True, 'placeholder': 'Confirm Password'}))
	
	class Meta:
		model = IbkUser
		fields = ('first_name', 'last_name', 'email', 'password', 'password2')
		fields_required = ('first_name', 'last_name',)
		widgets = {
			'first_name': forms.TextInput(attrs={'id': 'signup_first_name', 'placeholder': 'First Name', 'required': True}),
			'last_name': forms.TextInput(attrs={'id': 'signup_last_name', 'placeholder': 'Last Name', 'required': True}),
			'email': forms.EmailInput(attrs={'id': 'signup_email', 'placeholder': 'Enter Email'}),
			'password': forms.PasswordInput(attrs={'id': 'signup_password', 'placeholder': ' Enter Password'})
		}



