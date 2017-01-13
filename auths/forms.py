from django.forms import ModelForm
from django import forms


from accounts.models import IbkUser, Profile

class LoginAuthenticationForm(ModelForm):
	class Meta:
		model = IbkUser
		fields = ['username', 'password']
		fields_required = ('username')
		widgets = {
			'username': forms.TextInput(attrs={'id': 'login_username'}),
			'password': forms.PasswordInput(attrs={'id': 'login_password', 'placeholder': ' Enter Password'})
		}

