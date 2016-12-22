import os
import hashlib

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.core.signing import Signer, TimestampSigner
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from .models import IbkUser, Profile
from .forms	 import IbkUserSignUpForm

# Create your views here.
class AccountsIndex(TemplateView):
	template_name = 'accounts/base.html'

class AccountSignUp(CreateView):
	form_class = IbkUserSignUpForm
	template_name = 'accounts/signup_form.html'
	success_url = reverse_lazy('accounts:index')

	def generate_profile_validated_key(self, key_val):
		signer = TimestampSigner(salt=hashlib.sha1(os.urandom(16)).hexdigest())
		signed_value = signer.sign(key_val)
		sign_data, key_value = signed_value.split(':', 1)
		return key_value

	def generate_profile_key_link(self, key_val):
		active_key = get_object_or_404(Profile, verify_key=key_val)
		print(active_key)
		return active_key

	def form_valid(self, form):
		self.object = form.save()
		profile = Profile.objects.get(user_id=form.instance.id)
		profile.verify_key = self.generate_profile_validated_key(form.cleaned_data['email'])
		profile.save()
		user_context = {
			'name': form.name,
			'email': form.cleaned_data['email'],
			'key': profile.verify_key,
		}
		subject, from_email, to_email = 'Welcome to Ibhuku.com. Confrim your email.', 'noreply@ibhuku.com', form.cleaned_data['email']
		text_content = render_to_string('email/registration.txt', user_context).encode('utf-8')
		html_content = render_to_string('email/registration.html', user_context).encode('utf-8')
		msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
		msg.attach_alternative(html_content, "text/html")
		msg.send()
		return HttpResponseRedirect(self.get_success_url())