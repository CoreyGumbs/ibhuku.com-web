import hashlib
import os
from datetime import timedelta

from django.core.urlresolvers import resolve
from django.test import TestCase

from django.core.signing import Signer, TimestampSigner
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpRequest

from selenium import webdriver

from accounts.models import IbkUser, Profile
from accounts.views import AccountSignUp


#Test to see if app url '../accounts/' is responding
class IbkUserAccountsRedirectTest(TestCase):
	def test_index_redirect_status_code_to_register_view(self):
		response = self.client.get('/accounts/', follow=True)
		self.assertRedirects(response, '/accounts/register/')

	def test_redirect_uses_base_template(self):
		response = self.client.get('/accounts/', follow=True)
		self.assertTemplateUsed(response, 'accounts/base.html')

	def test_index_page_returns_correct_html(self):
		response = self.client.get('/accounts/', follow=True)
		html = response.content.decode('utf8')
		self.assertIn('<title>Sign-Up!</title>', html)
		self.assertTemplateUsed(response, 'accounts/base.html')

#Test of Accounts Registrations Views/URLs
class IbhukuRegistrationPageTest(TestCase):
	def test_sign_up_page_status_code(self):
		response = self.client.get('/accounts/register/')
		self.assertEqual(response.status_code, 200)

	def test_sign_up_view_uses_sign_up_template(self):
		response = self.client.get('/accounts/register/')
		self.assertTemplateUsed(response, 'accounts/signup_form.html')

	def test_registration_page_returns_correct_html(self):
		response = self.client.get('/accounts/register/')
		html = response.content.decode('utf8')
		self.assertIn('<title>Sign-Up!</title>', html)
		self.assertIn('submit', html)

	def test_account_validation_key_hashing(self):
		signer = Signer()
		key_value = signer.sign(self.profile.user.email)
		key = ''.join(key_value.split(':')[1:])
		self.assertEqual(self.profile.user.email, signer.unsign('{0}:{1}'.format(self.profile.user.email, key)))

class ActivationLinkResetTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.user = IbkUser.objects.create(email = "johndoe@test.com", name="John Doe", username="JohnnyBread", password="12345")
		cls.profile = Profile.objects.get(user_id=cls.user.id)
		cls.profile.verified = False
		cls.profile.save()

	def test_reset_page_verfified_exists(self):
		response = self.client.get('/accounts/reset/{0}'.format(self.profile.user_id))
		html = response.content.decode('utf8')
		self.assertIn('<title>Reset Activation Link</title>', html)
		self.assertEqual(response.status_code, 200)

	def test_profile_is_verified(self):
		self.profile.verified = True
		self.profile.key_value = 'expired'
		self.profile.save()
		self.assertTrue(self.profile.verified, True)
		self.assertEqual('expired', self.profile.key_value)
