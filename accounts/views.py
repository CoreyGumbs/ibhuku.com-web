import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils import timezone
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView
 
from .accountslib import confirm_account_link

from .models import IbkUser, Profile
from .forms	 import IbkUserSignUpForm, ResetActivationLinkForm

# Create your views here.
class CreateUserAccountView(CreateView):
	form_class = IbkUserSignUpForm
	template_name = 'accounts/signup_form.html'
	success_url = reverse_lazy('accounts:activation-sent')

	def form_valid(self, form):
		form.instance.name = form.instance.name.replace(' ', '')
		self.object = form.save()
		try:
			self.user = IbkUser.objects.get(email__iexact=form.instance.email)
			token = default_token_generator.make_token(self.user)
			if self.user:
				confirm_account_link(self.user, form.instance.email, token, request=self.request)
				return HttpResponseRedirect(self.get_success_url())
		except IbkUser.DoesNotExist:
			pass
		return HttpResponseRedirect(self.get_success_url())

def LinkActivationView(request, uidb64=None, token=None, token_generator=default_token_generator):
	try:
		user = IbkUser.objects.get(pk=force_text(urlsafe_base64_decode(uidb64)))
		profile = Profile.objects.get(user_id=user.pk)
	except (TypeError, ValueError, OverflowError, IbkUser.DoesNotExist):
		user =  None

	if user is not None and token_generator.check_token(user, token):
		validlink = True
		profile.verified = True
		profile.save()
	else:
		validlink = False

	context = {
		'validlink': validlink,
	}
	return render(request, 'accounts/verified_account.html', context)

def ResetActivationLink(request):
	if request.method == 'POST':
		form = ResetActivationLinkForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			try:
				user = IbkUser.objects.get(email__iexact=email)
				token = default_token_generator.make_token(user)
				if user:
					confirm_account_link(user, email, token, request=request)
					return HttpResponseRedirect(reverse('accounts:activation-sent'))
			except IbkUser.DoesNotExist:
				pass
			return HttpResponseRedirect(reverse('accounts:activation-sent'))
	else:
		form = ResetActivationLinkForm()
	
	context = {
		'form': form,
	}
	return render(request, 'accounts/reset_link_form.html', context)

class ActivationLinkSentMessage(TemplateView):
	template_name = 'accounts/activation_sent.html'

class AccountErrorMessage(TemplateView):
	template_name = 'accounts/account_error.html'


