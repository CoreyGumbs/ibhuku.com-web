from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from .models import IbkUser, Profile

# Create your views here.
class AccountsIndex(TemplateView):
	template_name = 'accounts/base.html'

class AccountSignUp(CreateView):
	form_class = UserCreationForm
	model = IbkUser
	template_name = 'accounts/registration.html'