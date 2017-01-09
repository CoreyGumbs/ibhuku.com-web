#!/usr/bin/env python
"""
Copyright (C) Corey Gumbs
AcountsLib or Accounts Library contains helper methods 
used in the accounts application. These helpers are used mainly
in the views business logic. 
"""
from django.conf import settings
from django.core.signing import Signer
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import Profile


def profile_validation_key(user_key):
	"""
	Used for generating a validation key that is emailed to user
	to verify their account after creating an account.
	"""
	signer = Signer(salt= settings.USER_SALT)
	signed_value = signer.sign(user_key)
	verification = ''.join(signed_value.split(':')[1:])
	return verification

def check_profile_validation_key(user_email, user_key):
	"""
	Checks generated profile_validation_key() against user account email and saved 'verify_key' in the Profiles model.
	Unsigns the verify_key data in Profile model and returns the confirming key.
	"""
	signer = Signer(salt= settings.USER_SALT)
	check_key = signer.unsign('{0}:{1}'.format(user_email, user_key))
	return check_key

def account_validation_email(name, email, key):
	"""
	Generates an account confirmation email upon user account creation. 
	"""
	user_context = {
			'name': name,
			'email': email,
			'key': key,
		}
	subject, from_email, to_email = 'Welcome to Ibhuku.com. Confirm your email.', 'noreply@ibhuku.com', email
	text_content = render_to_string('emails/registration.txt', user_context)
	html_content = render_to_string('emails/registration.html', user_context)
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
	msg.attach_alternative(html_content, "text/html")
	msg.send()

def authorized_view_session_check(valid_session):
	try:
		if valid_session is True:
			return True
		else:
			return False
	except KeyError:
		return False

def authorize_view_profile_check(valid_profile):
	try:
		profile = Profile.objects.get(user_id=valid_profile)
		if profile:
			return True
	except ObjectDoesNotExist:
		return False