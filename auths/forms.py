from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.core.validators import validate_email
from django.contrib.auth import password_validation

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button, Reset
from crispy_forms.bootstrap import FormActions, PrependedText

from accounts.models import IbkUser, Profile

class LoginAuthenticationForm(AuthenticationForm):
	"""
	A form that allows users to login to their accounts.
	"""
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

class AccountRecoveryForm(forms.Form):
	"""
	A form that allows users to recover their lost/forgotten password
	"""
	email = forms.EmailField(label='Email', max_length=255, required=True)
		
	def __init__(self, *args, **kwargs):
		super(AccountRecoveryForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'recoveryForm'
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
				PrependedText('email', "<span class='glyphicon glyphicon-envelope'></span>", active=True),
				FormActions(
					Submit('submit', 'Submit', css_class ='btn btn-success btn-lg btn-block'),
					),
			)

class PasswordResetForm(forms.Form):
	"""
	A form that allows user to change their old/forgotten password.
	"""
	new_password = forms.CharField(label='New Password', widget=forms.PasswordInput, strip=False,  help_text=password_validation.password_validators_help_text_html())
	confrim_new_password = forms.CharField(label='Confrim Password', widget=forms.PasswordInput, strip=False)

	def clean_confirm_new_password(self):
		new_password = self.cleaned_data.get('new_password')
		confrim_new_password = self.cleaned_data('confrim_new_password')

	def __init__(self, *args, **kwargs):
		super(PasswordResetForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'resetForm'
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
				PrependedText('new_password', "<span class='glyphicon glyphicon-lock'></span>", active=True),
				PrependedText('confrim_new_password', "<span class='glyphicon glyphicon-lock'></span>", active=True),
				FormActions(
					Submit('submit', 'Submit', css_class ='btn btn-success btn-lg btn-block'),
					),
			)





