from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

from .forms import LogInForm

# Create your views here.
def ProfileLogin(request):
	return HttpResponse('test')