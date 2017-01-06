#!/usr/bin/env python
import time
from datetime import timedelta
from importlib import import_module

from django.conf import settings
from django.core.signing import Signer, TimestampSigner
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.hashers import make_password, check_password
from django.test import TestCase, Client, RequestFactory
from django.http import HttpRequest

from accounts.accountslib import profile_validation_key
from accounts.models import IbkUser, Profile
from accounts.views import AccountSignUp


class TestModelFixtures(TestCase):
	"""
	Sets up user data fixtures for testing account models. Test will inherit from this class all
	pre-created user data.
	"""
	def setUp(self):
		self.factory = RequestFactory()
		self.client = Client()
		self.session = self.client.session
		self.session['active'] =  True
		self.session.save()

	@classmethod 
	def setUpTestData(cls):
		cls.user = IbkUser.objects.create(email = "mctest@test.com", name="McTest McTesty", username="McTestyRocks", password="12345")
		cls.user.password = make_password(cls.user.password, salt='jRkSlAw7KZ')
		cls.user.save()
		cls.profile = Profile.objects.get(user_id=cls.user.id)

class TestProfileValidationKey(TestModelFixtures):
	"""
	Test profile_validation_key() found in the accountslib.py module.
	Uses Django Signer to 'hash' email. To unsign hash, check_key, joins
	the email to the 'hash' for decoding. 
	User email should equal decoded (check_key) hash.
	"""
	def test_validation_key(self):
		valid_key = profile_validation_key(self.user.email)
		signer = Signer(salt= settings.USER_SALT)
		check_key = signer.unsign('{0}:{1}'.format(self.user.email, valid_key))
		self.assertEqual(check_key, self.user.email)

class TestAccountsIndexPage(TestModelFixtures):
	"""
	Test the url '/accounts/' redirects to the sign-up/register page.
	"""
	def test_accounts_url_redirects_to_register_view(self):
		response = self.client.get('/accounts/', follow=True)
		self.assertRedirects(response, '/accounts/register/')
		self.assertEqual(response.status_code, 200)

	def test_accounts_index_template(self):
		response = self.client.get('/accounts/', follow=True)
		self.assertTemplateUsed(response, 'accounts/signup_form.html')

	def test_accounts_index_content(self):
		response = self.client.get('/accounts/', follow=True)
		html = response.content.decode('utf8')
		self.assertIn('<title>Sign-Up!</title>', html)

class TestAccountSignUpView(TestModelFixtures):
	
	def test_sign_up_view(self):
		response = self.client.get('/accounts/register/')
		self.assertEqual(response.status_code, 200)


class TestActivationLinkSentView(TestModelFixtures):
	"""
	Test ActivationLinkSent message view. This view uses session cookie (session['active'] = True)
	to test if newly created account is active. If True, the link sent message appears. If false, redirects
	unauthorized users to the login page.
	"""
	def test_view_can_be_viewed_by_new_account(self):
		response = self.client.get('/accounts/sent/')
		self.assertEqual(response.status_code, 200, msg="Should show view message template")

	def test_view_cannot_be_accessed_anonymously(self):
		self.session['active'] =  False
		self.session.save()
		response = self.client.get('/accounts/sent/', follow=True)
		self.assertRedirects(response, '/profiles/login/?next=/accounts/sent/')

class TestVerifiedAccountMessageView(TestModelFixtures):
	"""
	Test VerifiedAccountMessage view. This view uses session cookie (session['active'] = True)
	to test if newly verified account is active. If True, the verified message appears. If false, redirects
	unauthorized users to the login page.
	"""

	def test_view_can_be_viewed_by_newly_activated_account(self):
		response = self.client.get('/accounts/verified/')
		self.assertEqual(response.status_code, 200)

	def test_verified_view_cannot_be_accessed_anonymously(self):
		self.session['active'] =  False
		self.session.save()
		response = self.client.get('/accounts/verified/', follow=True)
		self.assertRedirects(response, '/profiles/login/?next=/accounts/verified/')

class TestAccountErrorMessageView(TestCase):
	def test_acccount_error(self):
		response = self.client.get('/accounts/error/')
		self.assertEqual(response.status_code, 200)

	def test_account_error_template(self):
		response = self.client.get('/accounts/error/')
		html = response.content.decode('utf8')
		self.assertTemplateUsed('accounts/account_error.html')
		self.assertIn('<title>Account Error</title>', html)



# #Test of Accounts Registrations Views/URLs
# class IbhukuRegistrationPageTest(TestCase):
# 	def test_sign_up_page_status_code(self):
# 		response = self.client.get('/accounts/register/')
# 		self.assertEqual(response.status_code, 200)

# 	def test_sign_up_view_uses_sign_up_template(self):
# 		response = self.client.get('/accounts/register/')
# 		self.assertTemplateUsed(response, 'accounts/signup_form.html')

# 	def test_registration_page_returns_correct_html(self):
# 		response = self.client.get('/accounts/register/')
# 		html = response.content.decode('utf8')
# 		self.assertIn('<title>Sign-Up!</title>', html)
# 		self.assertIn('submit', html)

# 	def test_account_validation_key_hashing(self):
# 		signer = Signer()
# 		key_value = signer.sign(self.profile.user.email)
# 		key = ''.join(key_value.split(':')[1:])
# 		self.assertEqual(self.profile.user.email, signer.unsign('{0}:{1}'.format(self.profile.user.email, key)))

# class ActivationLinkResetTest(TestCase):
# 	@classmethod
# 	def setUpTestData(cls):
# 		cls.user = IbkUser.objects.create(email = "johndoe@test.com", name="John Doe", username="JohnnyBread", password="12345")
# 		cls.profile = Profile.objects.get(user_id=cls.user.id)
# 		cls.profile.verified = False
# 		cls.profile.save()

# 	def test_reset_page_verfified_exists(self):
# 		response = self.client.get('/accounts/reset/{0}'.format(self.profile.user_id))
# 		html = response.content.decode('utf8')
# 		self.assertIn('<title>Reset Activation Link</title>', html)
# 		self.assertEqual(response.status_code, 200)

# 	def test_profile_is_verified(self):
# 		self.profile.verified = True
# 		self.profile.key_value = 'expired'
# 		self.profile.save()
# 		self.assertTrue(self.profile.verified, True)
# 		self.assertEqual('expired', self.profile.key_value)
