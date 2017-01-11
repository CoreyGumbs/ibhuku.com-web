from django.test import TestCase, Client

from accounts.models import IbkUser, Profile
from profiles.views import ProfileLogin

class TestAccountLoginView(TestCase):
	"""
	Test Login View and account authentication.
	"""

	def test_account_login_view_url_responds(self):
		response = self.client.get('/profiles/login/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.resolver_match.url_name, 'login')
		self.assertEqual(response.resolver_match.func, ProfileLogin)