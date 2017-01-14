from django.shortcuts import render
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login

from .forms import LoginAuthenticationForm

# Create your views here.
def LoginView(request):
	if request.POST or None:
		form = LoginAuthenticationForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect(reverse('accounts:index'))
	else:
		form = LoginAuthenticationForm()
	context = {
		'form': form,
	}
	return render(request, 'auths/login.html', context)