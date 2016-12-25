from django.test import TestCase, Client
from django.core.urlresolvers import resolve


# Create your tests here.
class LocalHostServerTest(TestCase):
	def test_localserver(self):
		response = self.client.get('/accounts/')
		self.assertEqual(response.status_code, 200)