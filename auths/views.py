from django.shortcuts import render
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login

from .forms import LoginAuthenticationForm

# Create your views here.
def LoginView(request):
	if request.method == 'POST':
		form = LoginAuthenticationForm(data=request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			print(user)
			login(request, user)
			return HttpResponseRedirect(reverse('accounts:index'))
	else:
		form = LoginAuthenticationForm()
	context = {
		'form': form,
	}
	return render(request, 'auths/login.html', context)