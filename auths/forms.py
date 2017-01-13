from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm


from accounts.models import IbkUser, Profile

class LoginAuthenticationForm(AuthenticationForm):
	class Meta:
		fields = ['username', 'password']

