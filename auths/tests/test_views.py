from django.test import TestCase, Client
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.conf import settings

from accounts.models import IbkUser, Profile
from auths.views import AccountRecover

# Create your tests here.

class TestDataFixture(TestCase):
	"""
	Sets up user data fixtures for testing.
	"""
	def setUp(self):
		self.client = Client()

	@classmethod 
	def setUpTestData(cls):
		cls.user = IbkUser.objects.create_user(email = "mctest@test.com", name="McTest McTesty", username="McTestyRocks", password="password12345")

class LoginView(TestDataFixture):
	"""
	Test Login Authentication View
	"""
	def test_login_url(self):
		response = self.client.get('/auths/login/')
		self.assertEqual(response.status_code, 200)

	def test_login_view(self):
		response = self.client.get('/auths/login/')
		self.assertEqual(response.resolver_match.func.__name__, 'login')

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
		self.assertRedirects(response, '/accounts/register/')

class AccountRecover(TestDataFixture):
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
		

