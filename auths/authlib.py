#!/usr/bin/env python
"""
Copyright (C) 2017 Corey Gumbs
AuthsLib or Auths Library contains helper methods 
used in the auths application. These helpers are used mainly
in the views business logic. 
"""
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from accounts.models import IbkUser, Profile

def ValidateEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def password_reset_link(user, email, token, use_https=False, request=None):
	current_site = get_current_site(request)
	site_name = current_site.name
	domain = current_site.domain
	context = {
		'user': user,
	 	'token': token,
	 	'uid': urlsafe_base64_encode(force_bytes(user.pk)),
	 	'protocol': 'https' if use_https else 'http',
	 	'domain': domain,
	 	'site_name': site_name,
	}
	subject, from_email, to_email = 'A password reset was requested at Ibhuku.com', 'Ibhuku Team <noreply@ibhuku.com>', email
	text_content = render_to_string('email/password_reset_text.txt', context)
	html_content = render_to_string('email/password_reset_email.html', context)
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
	msg.attach_alternative(html_content, "text/html")
	msg.send()
		







