from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button, Reset
from crispy_forms.bootstrap import FormActions, PrependedText

from accounts.models import IbkUser, Profile

class LogInForm(AuthenticationForm):
	class Meta:
		model = IbkUser
		fields = ('username', 'password')
		widgets = {
			'username': forms.EmailInput(attrs={'id': 'login_email'}),
			'password': forms.PasswordInput(attrs={'id': 'login_password', 'placeholder': ' Enter Password'})
		}

	def __init__(self, *args, **kwargs):
		super(LogInForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'loginForm'
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
				PrependedText('username', "<span class='glyphicon glyphicon-envelope'></span>", placeholder="Email", active=True),
				PrependedText('password', "<span class='glyphicon glyphicon-lock'></span>", placeholder="Password", active=True),
				FormActions(
					Submit('submit', 'Login', css_class ='btn btn-success btn-lg btn-block'),
					),
			)

