import os
import hashlib
import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.core import signing
from django.core.signing import Signer, TimestampSigner, BadSignature
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.template.loader import render_to_string
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from .models import IbkUser, Profile
from .forms	 import IbkUserSignUpForm, ResetEmailActivationLinkForm

# Create your views here.
class AccountSignUp(CreateView):
	form_class = IbkUserSignUpForm
	template_name = 'accounts/signup_form.html'
	success_url = reverse_lazy('accounts:activation-sent')

	def generate_profile_validation_key(self, key_val):
		signer = Signer(salt= settings.USER_SALT)
		signed_value = signer.sign(key_val)
		key_value = ''.join(signed_value.split(':')[1:])
		return key_value

	def form_valid(self, form):
		form.instance.name = form.instance.name.replace(' ', '')
		self.object = form.save()
		self.request.session['active'] = form.instance.is_active
		profile = Profile.objects.get(user_id=form.instance.id)
		profile.verify_key = self.generate_profile_validation_key(form.instance.email)
		profile.save()
		user_context = {
			'name': form.instance.name,
			'email': form.cleaned_data['email'],
			'key': profile.verify_key,
		}
		subject, from_email, to_email = 'Welcome to Ibhuku.com. Confirm your email.', 'noreply@ibhuku.com', form.cleaned_data['email']
		text_content = render_to_string('emails/registration.txt', user_context)
		html_content = render_to_string('emails/registration.html', user_context)
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
		msg.attach_alternative(html_content, "text/html")
		msg.send()
		return HttpResponseRedirect(self.get_success_url())

def AccountActivation(request, verify_key):
	try:
		profile = Profile.objects.get(verify_key=verify_key)
		signer = Signer(salt= settings.USER_SALT)
		check_key = signer.unsign('{0}:{1}'.format(profile.user.email, profile.verify_key))
		if check_key == profile.user.email and profile.expire_date > timezone.now():
			profile.verified = True
			profile.verify_key = 'expired'
			profile.save()
			return HttpResponseRedirect(reverse('accounts:verified'))
	except ObjectDoesNotExist:
		try:
			profile = Profile.objects.get(verify_key='expired')
			if profile.verify_key == 'expired':
				return HttpResponseRedirect(reverse('accounts:verified'))
		except:
			return HttpResponseRedirect(reverse('accounts:account-error'))
	except:
		return HttpResponseRedirect(reverse('accounts:verified'))
	return HttpResponseRedirect(reverse('accounts:link_reset', args=[profile.user_id]))

class ResetLinkActivation(CreateView):
	form_class = ResetEmailActivationLinkForm
	template_name = 'accounts/reset_link_form.html'
	success_url = reverse_lazy('accounts:activation-sent')

	def generate_profile_validation_key(self, key_val):
		signer = Signer(salt= settings.USER_SALT)
		signed_value = signer.sign(key_val)
		key_value = ''.join(signed_value.split(':')[1:])
		return key_value

	def form_valid(self, form):
		try:
			profile = Profile.objects.get(user_id=self.kwargs['user_id'])
			if profile.verified is True:
				return HttpResponseRedirect(reverse('accounts:verified'))
			else:
				profile.verify_key = self.generate_profile_validation_key(profile.user.email)
				profile.expire_date = timezone.now() + datetime.timedelta(days=3)
				profile.save()
				user_context = {
					'name': profile.user.name,
					'email': profile.user.email,
					'key': profile.verify_key,
				}
				subject, from_email, to_email = 'Welcome to Ibhuku.com. Confirm your email.', 'noreply@ibhuku.com', profile.user.email
				text_content = render_to_string('emails/registration.txt', user_context)
				html_content = render_to_string('emails/registration.html', user_context)
				msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
				msg.attach_alternative(html_content, "text/html")
				msg.send()
		except ObjectDoesNotExist:
			return HttpResponseRedirect(reverse('accounts:account-error'))
		except:
			return HttpResponseRedirect(reverse('accounts:link_reset', args=[profile.user_id]))
		return HttpResponseRedirect(reverse('accounts:activation-sent'))


class ActivationLinkSentMessage(UserPassesTestMixin, TemplateView):
	template_name = 'accounts/activation_sent.html'
	def test_func(self):
		"""
		Once account is created, session is set to active. 
		Tests to see if session is active. If True, allows sent
		message to be seen by user else it will redirect to login page.
		"""
		try:
			if self.request.session['active'] is True:
				return True
			else:
				return False
		except KeyError:
			return False

class VerifiedAccountMessage(UserPassesTestMixin, TemplateView):
	template_name = 'accounts/verified_account.html'
	def test_func(self):
		"""
		Once account is created, session is set to active. 
		Tests to see if session is active. If True, allows sent
		message to be seen by user else it will redirect to login page.
		"""
		try:
			if self.request.session['active'] is True:
				return True
			else:
				return False
		except KeyError:
			return False

class AccountErrorMessage(TemplateView):
	template_name = 'accounts/account_error.html'


