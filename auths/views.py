from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import LoginAuthenticationForm

# Create your views here.
def LoginView(request):
	context = {
		'form': 'form',
	}
	return render(request, 'auths/login.html', context)