from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button, Reset
from crispy_forms.bootstrap import FormActions, PrependedText

from accounts.models import IbkUser, Profile

class LoginAuthenticationForm(forms.Form):
	email = forms.EmailField(label='Email', required=True)
	password = forms.CharField(label='Password', required=True)
	
	class Meta:
		widgets = {
			'email': forms.TextInput(attrs={'id': 'login_username'}),
			'password': forms.PasswordInput(attrs={'id': 'login_password', 'placeholder': ' Enter Password'})
		}

	def __init__(self, *args, **kwargs):
		super(LoginAuthenticationForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'loginForm'
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
				PrependedText('email', "<span class='glyphicon glyphicon-envelope'></span>", placeholder="Email", active=True),
				PrependedText('password', "<span class='glyphicon glyphicon-lock'></span>", placeholder="Password", active=True),
				FormActions(
					Submit('submit', 'Submit', css_class ='btn btn-success btn-lg btn-block'),
					),
			)

