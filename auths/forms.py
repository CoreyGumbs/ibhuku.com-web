from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button, Reset
from crispy_forms.bootstrap import FormActions, PrependedText

from accounts.models import IbkUser, Profile

class LoginAuthenticationForm(AuthenticationForm):
	username = forms.EmailField(label='Email', required=True, widget=forms.TextInput(attrs={'id': 'login_username'}))
	password = forms.CharField(label='Password', required=True,widget=forms.PasswordInput(attrs={'id': 'login_password'}))

	def __init__(self, *args, **kwargs):
		super(LoginAuthenticationForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'loginForm'
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
				PrependedText('username', "<span class='glyphicon glyphicon-envelope'></span>", active=True),
				PrependedText('password', "<span class='glyphicon glyphicon-lock'></span>", active=True),
				FormActions(
					Submit('submit', 'Submit', css_class ='btn btn-success btn-lg btn-block'),
					),
			)

