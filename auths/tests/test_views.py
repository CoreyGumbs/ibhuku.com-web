
#!/usr/bin/env python
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.core.urlresolvers import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings

from accounts.models import IbkUser, Profile
from auths.views import AccountRecover, AccountResetLinkConfirm, AccountLogin
from auths.forms import UserPasswordResetForm
from auths.authlib import ValidateEmail

# Create your tests here.

class TestDataFixture(TestCase):
	"""
	Sets up user data fixtures for testing.
	"""
	def setUp(self):
		self.client = Client()
		self.factory = RequestFactory()

	@classmethod 
	def setUpTestData(cls):
		cls.user = IbkUser.objects.create_user(email = "mctest@test.com", name="McTestMcTesty", username="McTestyRocks", password="password12345")
		cls.user_token = default_token_generator.make_token(cls.user)
		cls.uid = urlsafe_base64_encode(force_bytes(cls.user.pk))
		cls.profile = Profile.objects.get(user_id=cls.user.id)

class TestLoginView(TestDataFixture):
	"""
	Test Login Authentication View
	"""
	def test_login_url(self):
		response = self.client.get('/auths/login/')
		self.assertEqual(response.status_code, 200)

	def test_login_view(self):
		response = self.client.get('/auths/login/')
		self.assertEqual(response.resolver_match.func.__name__, 'AccountLogin')

	def test_login_view_html(self):
		response = self.client.get('/auths/login/')
		html = response.content.decode('utf8')
		self.assertIn('<title>Login</title>', html)

	def test_login_view_template(self):
		response = self.client.get('/auths/login/')
		self.assertTemplateUsed(response, 'auths/login.html')

	def test_user_login_view(self):
		login = self.client.login(username='mctest@test.com', password='password12345')
		response = self.client.post('/auths/login/', {'username':'mctest@test.com', 'password':'password12345'}, follow=True)
		self.assertEqual(response.context['user'].email, self.user.email)
		self.assertIs(response.context['user'].is_active, True)
		self.assertIs(login, True)
	
	def test_user_login_view_redirect(self):
		response = self.client.post('/auths/login/', {'username':'mctest@test.com', 'password':'password12345'}, follow=True)
		self.assertRedirects(response, '/profile/McTestMcTesty')

	def test_invalid_user_login(self):
		response = self.client.post('/auths/login/', {'username':'john@test.com', 'password':'password12345'})
		html = response.content.decode('utf8')
		self.assertIn('The username or password you entered are incorrect.', html) 

class TestAccountRecover(TestDataFixture):
	"""
	Test Password Reset View
	"""
	def test_account_recover_url(self):
		response = self.client.get('/auths/recover/')
		self.assertEqual(response.status_code, 200)

	def test_account_recover_html(self):
		response =self.client.get('/auths/recover/')
		html = response.content.decode('utf8')
		self.assertIn('<title>Recover Account</title>', html)

	def test_account_recover_template(self):
		response = self.client.get('/auths/recover/')
		self.assertTemplateUsed(response, 'auths/recover.html')

	def test_account_recover_view(self):
		response = self.client.get('/auths/recover/')
		self.assertEqual(response.resolver_match.func.__name__, 'AccountRecover')

	def test_account_recover_context(self):
		response = self.client.get('/auths/recover/')
		self.assertIn('Email:' , str(response.context['form']))

	def test_user_exists(self):
		response = self.client.post('/auths/recover/', {'email': 'mctest@test.com'}, follow=True)
		self.assertRedirects(response, '/auths/recover/done/')


class TestAccountResetLinkConfirm(TestDataFixture):
	"""
	Test Password Link Confirmation View
	"""
	def test_reset_link_confirm_view_url(self):
		response = self.client.post(reverse('auths:recover-password', kwargs={'uidb64': self.uid, 'token': self.user_token}))
		self.assertEqual(response.status_code, 200)

	def test_reset_link_confirm_view(self):
		response = self.client.post(reverse('auths:recover-password', kwargs={'uidb64': self.uid, 'token': self.user_token}))
		self.assertEqual(response.resolver_match.func.__name__, 'AccountResetLinkConfirm')

	def test_reset_link_confirm_view_html(self):
		response = self.client.post(reverse('auths:recover-password', kwargs={'uidb64': self.uid, 'token': self.user_token}))
		html = response.content.decode('utf8')
		self.assertIn('<title>Password Reset</title>', html)

	def test_reset_link_confrim_view_url(self):
		response = self.client.post(reverse('auths:recover-password', kwargs={'uidb64': self.uid, 'token': self.user_token}))
		self.assertTemplateUsed(response, 'auths/password_reset_confirm.html')

	def test_reset_link_confirm_context(self):
		response = self.client.post(reverse('auths:recover-password', kwargs={'uidb64': self.uid, 'token': self.user_token}))
		self.assertIn('New Password:', str(response.context['form']))

	def test_reset_link_confirm_user_uidb64_error_redirect(self):
		response = self.client.post(reverse('auths:recover-password', kwargs={'uidb64': b'MXM', 'token': self.user_token}))
		html = response.content.decode('utf8')
		self.assertIs(response.context['validlink'], False)
		self.assertIs(response.context['form'], None)
		self.assertIn('Please request a new password reset' ,html)






