from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import IbkUser


class IbkUserSignUpForm(ModelForm):
	password2 = forms.CharField(label=_('Confirm Password'), widget=forms.PasswordInput())
	class Meta:
		model = IbkUser
		fields = ('first_name', 'last_name', 'email', 'password', 'password2')
