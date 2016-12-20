from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.core.signing import Signer
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from .models import IbkUser, Profile
from .forms	 import IbkUserSignUpForm

# Create your views here.
class AccountsIndex(TemplateView):
	template_name = 'accounts/base.html'

class AccountSignUp(CreateView):
	form_class = IbkUserSignUpForm
	template_name = 'accounts/signup_form.html'
	success_url = reverse_lazy('accounts:index')

	def generate_profile_validated_key(self):
		profile  = Profile.objects.get(user_id=request.user.id)
		return profile