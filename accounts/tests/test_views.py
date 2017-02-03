#!/usr/bin/env python
import time
from django.conf import settings
from django.test import TestCase, Client
from django.core import mail
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


from accounts.views import CreateUserAccountView, LinkActivationView
from accounts.models import IbkUser, Profile
from accounts.accountslib import confirm_account_link

class TestModelFixtures(TestCase):
	"""
	Sets up user data fixtures for testing account models. Test will inherit from this class all
	pre-created user data.
	"""
	def setUp(self):
		self.client = Client()

	@classmethod 
	def setUpTestData(cls):
		cls.user = IbkUser.objects.create(email = "mctest@test.com", name="McTest McTesty", username="McTestyRocks", password="12345")
		cls.user_token = default_token_generator.make_token(cls.user)
		cls.uid = urlsafe_base64_encode(force_bytes(cls.user.pk))
		cls.profile = Profile.objects.get(user_id=cls.user.id)

class TestCreateUserAccount(TestCase):
	"""
	Test of the user creation view.
	"""
	def setUp(self):
		self.client = Client()

	def test_accounts_url_redirects_to_register_view(self):
		response = self.client.get('/accounts/', follow=True)
		self.assertRedirects(response, '/accounts/register/')
		self.assertEqual(response.status_code, 200, msg='return page is working')

	def test_create_user_view_url(self):
		response = self.client.get('/accounts/register/')
		self.assertEqual(response.status_code, 200, msg='Returns 200 if page found.')
		self.assertEqual(response.resolver_match.func.__name__, 'CreateUserAccountView')

	def test_create_user_template(self):
		response = self.client.get('/accounts/register/')
		self.assertTemplateUsed(response, 'accounts/signup_form.html')

	def test_create_user_view_template(self):
		response = self.client.get('/accounts/register/')
		html = response.content.decode('utf-8')
		self.assertIn('<title>Sign-Up!</title>', html, msg='Should return correct page <title>')

	def test_create_user_view_redirection(self):
		response = self.client.post('/accounts/register/', {'name': 'Test', 'email': 'test@test.com', 'password': 'password12345'})
		self.assertRedirects(response, '/accounts/sent/')

	def test_user_creation_new_user_exists(self):
		response = self.client.post('/accounts/register/', {'name': 'Test', 'email': 'test@test.com', 'password': 'password12345'})
		new_user = IbkUser.objects.get(email='test@test.com')
		self.assertEqual(new_user.name, 'Test')

	def test_new_account_redirect_message(self):
		response = self.client.post('/accounts/register/', {'name': 'Test', 'email': 'test@test.com', 'password': 'password12345'}, follow=True)
		self.assertRedirects(response, '/accounts/sent/')

	def test_sent_view_html(self):
		response = self.client.get('/accounts/sent/')
		html = response.content.decode('utf-8')
		self.assertEqual(response.status_code, 200, msg="Should show view message template")
		self.assertIn('<h3>Your Activation Email Is On The Way.</h3>', html)

class TestLinkActivationView(TestModelFixtures):
	"""
	Test Email Activation Link View.
	"""
	def test_link_activation_view(self):
		response = self.client.post(reverse('accounts:activate', kwargs={'uidb64': self.uid, 'token': self.user_token}))
		self.assertEqual(response.resolver_match.func.__name__, 'LinkActivationView')
		self.assertEqual(response.resolver_match.kwargs, {'uidb64': force_text(self.uid), 'token': self.user_token})

	def test_link_activation_url(self):
		response = self.client.post(reverse('accounts:activate', kwargs={'uidb64': self.uid, 'token': self.user_token}))
		self.assertEqual(response.status_code, 200)

	def test_link_activation_template(self):
		response = self.client.post(reverse('accounts:activate', kwargs={'uidb64': self.uid, 'token': self.user_token}))
		self.assertTemplateUsed(response, 'accounts/verified_account.html')

	def test_link_activation_html(self):
		response = self.client.post(reverse('accounts:activate', kwargs={'uidb64': self.uid, 'token': self.user_token}))
		html = response.content.decode('utf-8')
		self.assertIn('<title>Verified Activation Link</title>', html)

	def test_link_activation_validitation_works(self):
		response = self.client.post(reverse('accounts:activate', kwargs={'uidb64': self.uid, 'token': self.user_token}))
		html = response.content.decode('utf-8')
		self.assertIs(response.context['validlink'], True)
		self.assertIn('<h2>Your Account Has Been Verified.</h2>', html)

	def test_link_activation_validation_error(self):
		response = self.client.post(reverse('accounts:activate', kwargs={'uidb64': b'MdP', 'token': self.user_token}))
		html = response.content.decode('utf-8')
		self.assertIs(response.context['validlink'], False)
		self.assertIn('<h2>Sorry there was an error.</h2>', html)

class TestResetActivationLinkView(TestModelFixtures):
	"""
	Test Reset of Activation Link View
	"""
	def test_reset_link_view_and_url(self):
		response = self.client.get('/accounts/reset/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.resolver_match.func.__name__, 'ResetActivationLink')

	def test_reset_link_view_template(self):
		response = self.client.get('/accounts/reset/')
		self.assertTemplateUsed('accounts/reset_link_form.html')

	def test_reset_link_view_html(self):
		response = self.client.get('/accounts/reset/')
		html = response.content.decode('utf-8')
		self.assertIn('<title>Reset Activation Link</title>', html)

	def test_reset_link_view_context(self):
		response = self.client.get('/accounts/reset/')
		self.assertIn('email', str(response.context['form']))

	def test_reset_link_view_redirect(self):
		response = self.client.post('/accounts/reset/', {'email': 'test@test.com'})
		self.assertRedirects(response, '/accounts/sent/')




