from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse, resolve, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.response import TemplateResponse
from django.views.generic.base import View, TemplateView


from accounts.models import IbkUser, Profile
from auths.authlib import password_reset_link
from auths.forms import LoginAuthenticationForm, AccountRecoveryForm, UserPasswordResetForm

# Create your views here.
@csrf_protect
def AccountLogin(request):
	form = LoginAuthenticationForm(request.POST or None)
	username = request.POST.get('username')
	password = request.POST.get('password')
	if request.POST and form.is_valid():
		user = form.login(request)
		if user:
			login(request, user)
			return redirect(reverse_lazy('profile:dashboard', kwargs={'name': request.user.name}))

	context = {
		'form': form,
	}
	return render(request, 'auths/login.html', context)

@csrf_protect
def AccountRecover(request):
	if request.method == 'POST':
		form = AccountRecoveryForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			try:
				user= IbkUser.objects.get(email__iexact=email)
				token = default_token_generator.make_token(user)
				if user:
					password_reset_link(user, email, token, request=request)
					return HttpResponseRedirect(reverse('auths:recover-done'))
			except IbkUser.DoesNotExist:
				return HttpResponseRedirect(reverse('auths:recover-done'))
	else:
		form = AccountRecoveryForm()
	context = {
		'form': form,
	}
	return render(request, 'auths/recover.html', context)

@csrf_protect
def AccountResetLinkConfirm(request, uidb64=None, token=None, token_generator=default_token_generator):
	form = None
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = IbkUser.objects.get(pk=uid)
		profile = Profile.objects.get(user_id=user.id)
	except (TypeError, ValueError, OverflowError, IbkUser.DoesNotExist):
		user = None

	if user is not None and token_generator.check_token(user, token):
		validlink = True
		if request.method == 'POST':
			form = UserPasswordResetForm(user, request.POST or None)
			if form.is_valid():
				form.save()
				profile.verified = True
				profile.save()
				return HttpResponseRedirect(reverse('auths:reset-complete'))
		else:
			form = UserPasswordResetForm(user)
	else:
		validlink = False

	context={
		'validlink': validlink,
		'form': form,
	}
	return TemplateResponse(request, 'auths/password_reset_confirm.html', context)

class PasswordResetDone(TemplateView):
	template_name = 'auths/password_reset_done.html'

class PasswordResetComplete(TemplateView):
	template_name = 'auths/password_reset_complete.html'