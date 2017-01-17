from django.shortcuts import render
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login

from .forms import LoginAuthenticationForm

# Create your views here.
def AccountRecover(request):
	return render(request, 'auths/recover.html')