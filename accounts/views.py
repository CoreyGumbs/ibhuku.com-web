import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView, UpdateView
 
from .accountslib import (profile_validation_key, account_validation_email, authorized_view_session_check, authorize_view_profile_check,check_profile_validation_key,)

from .models import IbkUser, Profile
from .forms	 import IbkUserSignUpForm, ResetEmailActivationLinkForm

# Create your views here.
class AccountSignUp(CreateView):
	form_class = IbkUserSignUpForm
	template_name = 'accounts/signup_form.html'
	success_url = reverse_lazy('accounts:activation-sent')

	def form_valid(self, form):
		form.instance.name = form.instance.name.replace(' ', '')
		self.object = form.save()
		self.request.session['active'] = form.instance.is_active
		profile = Profile.objects.get(user_id=form.instance.id)
		profile.verify_key = profile_validation_key(form.instance.email)
		profile.save()
		account_validation_email(form.cleaned_data['name'], form.cleaned_data['email'], profile.verify_key)
		return HttpResponseRedirect(self.get_success_url())

def AccountActivation(request, verify_key):
	try:
		profile = Profile.objects.get(verify_key=verify_key)
		check_key = check_profile_validation_key(profile.user.email, profile.verify_key)
		if check_key == profile.user.email and profile.expire_date > timezone.now():
			profile.verified = True
			profile.verify_key = 'expired'
			profile.save()
			return HttpResponseRedirect(reverse('accounts:verified'))
	except ObjectDoesNotExist:
		try:
			profile = Profile.objects.get(verify_key=verify_key)
			if profile.verify_key == 'expired':
				return HttpResponseRedirect(reverse('accounts:verified'))
		except:
			return HttpResponseRedirect(reverse('accounts:account-error'))
	return HttpResponseRedirect(reverse('accounts:link-reset', args=[profile.user_id]))

class ResetLinkActivation(UserPassesTestMixin, CreateView):
	form_class = ResetEmailActivationLinkForm
	template_name = 'accounts/reset_link_form.html'
	success_url = reverse_lazy('accounts:activation-sent')

	def test_func(self):
		"""
		Once account is created, session is set to active. 
		Tests to see if session is active. If True, allows sent
		message to be seen by user else it will redirect to login page.
		"""
		return authorize_view_profile_check(self.kwargs['user_id'])

	def get_login_url(self):
		try:  
			profile = Profile.objects.get(user_id=self.kwargs['user_id'])
			return super(ResetLinkActivation, self).get_login_url()
		except ObjectDoesNotExist:
			return '/accounts/error/'

	def form_valid(self, form):
		try:
			profile = Profile.objects.get(user_id=self.kwargs['user_id'])
			if profile.verified is True:
				return HttpResponseRedirect(reverse('accounts:verified'))
			else:
				profile.verify_key = profile_validation_key(profile.user.email)
				profile.expire_date = timezone.now() + datetime.timedelta(seconds=30)
				profile.save()
				account_validation_email(profile.user.name, profile.user.email, profile.verify_key)
		except ObjectDoesNotExist:
			return HttpResponseRedirect(reverse('accounts:account-error'))
		except:
			return HttpResponseRedirect(reverse('accounts:link-reset', args=[profile.user_id]))
		return HttpResponseRedirect(reverse('accounts:activation-sent'))


class ActivationLinkSentMessage(UserPassesTestMixin, TemplateView):
	template_name = 'accounts/activation_sent.html'
	def test_func(self):
		"""
		Once account is created, session is set to active. 
		Tests to see if session is active. If True, allows sent
		message to be seen by user else it will redirect to login page.
		"""
		return authorized_view_session_check(self.request.session['active'])
		
class VerifiedAccountMessage(UserPassesTestMixin, TemplateView):
	template_name = 'accounts/verified_account.html'
	def test_func(self):
		"""
		Once account is created, session is set to active. 
		Tests to see if session is active. If True, allows sent
		message to be seen by user else it will redirect to login page.
		"""
		return authorized_view_session_check(self.request.session['active'])

class AccountErrorMessage(TemplateView):
	template_name = 'accounts/account_error.html'


