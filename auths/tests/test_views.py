from django.test import TestCase, Client
from django.conf import settings

from accounts.models import IbkUser, Profile

# Create your tests here.
class LoginView(TestCase):
	"""
	Test Login Authentication View
	"""
	def test_url(self):
		response = self.client.get('/auths/login/')
		self.assertEqual(response.status_code, 200)

	def test_view_html(self):
		response = self.client.get('/auths/login/')
		html = response.content.decode('utf8')
		self.assertIn('<title>Login</title>', html)

