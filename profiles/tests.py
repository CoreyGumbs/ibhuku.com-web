from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


from accounts.models import IbkUser, Profile

# Create your tests here.
class UserProfileTestDataSetUp(TestCase):
	"""
	Sets up user and profile test data for Profiles app.
	Some test will inherit from this class for testing Profiles app views and logic.
	"""
	def setUp(self):
		self.factory = RequestFactory()
		self.client = Client()

	@classmethod
	def setUpTestData(cls):
		cls.user = IbkUser.objects.create(email = "johndoe@test.com", name="John Doe", username="JohnnyBread", password="12345")
		cls.profile = Profile.objects.get(user_id=cls.user.id)

	def test_profile_test_data(self):
		self.assertEqual(self.user.name, 'John Doe')
		self.assertEqual(self.profile.user.username, 'JohnnyBread')


class ProfileLoginTest(UserProfileTestDataSetUp):
	pass

