#!/usr/bin/env python
import time

from django.conf import settings
from django.core.signing import Signer
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.hashers import make_password, check_password
from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse, resolve
from django.views.generic.base import RedirectView

from accounts.accountslib import profile_validation_key, authorized_view_session_check, check_profile_validation_key
from accounts.models import IbkUser, Profile
from ..views import *



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

class TestProfileValidationAndCheckKeyFunctions(TestModelFixtures):
	"""
	Test profile_validation_key() and check_profile_validation_key()  found in the accountslib.py module.
	"""	
	def test_validation_key(self):
		"""
		Test profile_validation_key() found in the accountslib.py module.
		Uses Django Signer to 'hash' email. To unsign hash, check_key, joins
		the email to the 'hash' for decoding. 
		User email should equal decoded (check_key) hash.
		"""
		valid_key = profile_validation_key(self.user.email)
		signer = Signer(salt= settings.USER_SALT)
		check_key = signer.unsign('{0}:{1}'.format(self.user.email, valid_key))
		self.assertEqual(check_key, self.user.email, msg='Newly created key decoded, should match email')

	def test_check_validation_key(self):
		"""
		Test check_profile_validation_key() found in accountslib.py module
		Checks generated profile_validation_key() against user account email and saved 'verify_key' in the Profiles model.
		Unsigns the verify_key data in Profile model and returns the confirming key.
		"""
		valid_key = profile_validation_key(self.user.email)
		check_key = check_profile_validation_key(self.user.email, valid_key)
		self.assertEqual(self.user.email, check_key, msg='Should decode key and match email')

class TestAuthorizedViewSessionCheckFunction(TestModelFixtures):
	"""
	Test is session['active'] is True or False. The result determines if
	True or False for test_func permission on class views. These permissions
	dictate if the particular view can be seen by an authorized user or not. 
	"""
	def test_session_check(self):
		valid_session = authorized_view_session_check(self.session['active'])
		self.assertTrue(valid_session, msg='Should return active session is True')

	def test_invalid_session_check(self):
		self.session['active'] =  False
		self.session.save()
		valid_session = authorized_view_session_check(self.session['active'])
		self.assertFalse(valid_session, msg="Should return active session False")

class TestAccountsIndexViewRedirection(TestModelFixtures):
	"""
	Test the url '/accounts/' redirects to the sign-up/register page.
	Uses RedirectView located in the accouts/urls.py module.
	"""
	def test_accounts_url_redirects_to_register_view(self):
		response = self.client.get('/accounts/', follow=True)
		self.assertRedirects(response, '/accounts/register/')
		self.assertEqual(response.status_code, 200, msg='return page is working')

	def test_accounts_index_template(self):
		response = self.client.get('/accounts/', follow=True)
		self.assertTemplateUsed(response, 'accounts/signup_form.html')

	def test_accounts_index_content(self):
		response = self.client.get('/accounts/', follow=True)
		html = response.content.decode('utf8')
		self.assertIn('<title>Sign-Up!</title>', html, msg='Should return correct page title')

class TestAccountSignUpView(TestModelFixtures):
	"""
	Test the '/accounts/register/' view for registering new account.
	"""
	def test_sign_up_view(self):
		response = self.client.get('/accounts/register/')
		self.assertEqual(response.status_code, 200, msg='return page is working')

	def test_view_returns_template(self):
		response = self.client.get('/accounts/register/')
		self.assertTemplateUsed(response, 'accounts/signup_form.html')

	def test_correct_html(self):
		response = self.client.get('/accounts/register/')
		html = response.content.decode('utf8')
		self.assertIn('<title>Sign-Up!</title>', html, msg='Should return correct page title')

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
		self.assertEqual(response.status_code, 200, msg='return page is working')

	def test_verified_view_cannot_be_accessed_anonymously(self):
		self.session['active'] =  False
		self.session.save()
		response = self.client.get('/accounts/verified/', follow=True)
		self.assertRedirects(response, '/profiles/login/?next=/accounts/verified/')

	def test_account_verified(self):
		self.profile.verified = True
		self.profile.key_value = 'expired'
		self.profile.save()
		self.assertTrue(self.profile.verified, msg='should return True')
		self.assertEqual('expired', self.profile.key_value, msg='Should return expired')

class TestAccountErrorMessageView(TestCase):
	"""
	Test Account Error Message View.
	"""
	def test_acccount_error(self):
		response = self.client.get('/accounts/error/')
		self.assertEqual(response.status_code, 200, msg='return page is working')

	def test_account_error_template(self):
		response = self.client.get('/accounts/error/')
		html = response.content.decode('utf8')
		self.assertTemplateUsed('accounts/account_error.html')
		self.assertIn('<title>Account Error</title>', html)


class TestResetLinkActivationView(TestModelFixtures):
	"""
	Test Reset Link View Page. 
	"""
	def test_reset_view_without_parameter_redirects(self):
		response = self.client.get('/accounts/reset/', follow=True)
		html =response.content.decode('utf8')
		self.assertEqual(response.status_code, 200, msg='return page is working')
		self.assertRedirects(response, '/accounts/error/')
		self.assertIn('<h2>Your Account Could Not Be Found.</h2>', html, msg='Should return correct div heading')

	def test_reset_view_account_error_redirects(self):
		response = self.client.get('/accounts/reset/1/', follow=True)
		self.assertEqual(response.status_code, 200, msg='return page is working')
		self.assertRedirects(response, '/accounts/error/?next=/accounts/reset/1/')

	def test_reset_view_account_correct_parameter(self):
		response = self.client.get(reverse('accounts:link-reset', kwargs={'user_id' : self.profile.user_id}))
		html = response.content.decode('utf8')
		self.assertEqual(response.status_code, 200, msg='return page is working')
		self.assertIn('<h2>Reset Acccount Activation Link</h2>', html, msg='Should return correct div heading')
		self.assertEqual(response.resolver_match.func.__name__, ResetLinkActivation.as_view().__name__, msg='returns correct url/view name')

class TestAcccountActivationView(TestModelFixtures):
	"""
	Test that account is verified via user email link.
	"""
	def test_account_activation_view_without_parameter_redirects(self):
		response = self.client.get('/accounts/activation/', follow=True)
		self.assertEqual(response.status_code, 200, msg='return page is working')
		self.assertRedirects(response, '/accounts/error/')
		self.assertEqual(response.resolver_match.func.__name__, AccountErrorMessage.as_view().__name__, msg="Should match correct url/view name")

	def test_account_verification_view_new_account_verfied_redirect(self):
		self.profile.verify_key = profile_validation_key(self.user.email)
		self.profile.save()
		response = self.client.get(reverse('accounts:activation', kwargs={'verify_key': self.profile.verify_key}))
		self.assertEqual(response.status_code, 302, msg='return page is working')
		self.assertEqual(response.resolver_match.kwargs, {'verify_key': self.profile.verify_key}, msg='Should match passed parameters')
		self.assertRedirects(response, '/accounts/verified/')



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
