from django.test import TestCase

from accounts.models import IbkUser, Profile
from auths.forms import LoginAuthenticationForm
# Create your tests here.

class TestModelFixtures(TestCase):
	"""
	Sets up user data fixtures for testing account models. Test will inherit from this class all
	pre-created user data.
	"""
	def setUp(self):
		self.client = Client()

	@classmethod 
	def setUpTestData(cls):
		cls.user = IbkUser.objects.create(email = "mctest@test.com", name="McTest McTesty", username="McTestyRocks", password="password12345")
		cls.profile = Profile.objects.get(user_id=cls.user.id)
		cls.profile.save()

class TestLoginAuthenticationForm(TestModelFixtures):
	"""
	Test Ibhuku Account Login Form
	"""
	def setUp(self):
		self.form = LoginAuthenticationForm()

	def test_form_is_un_bound(self):
		self.assertIs(self.form.is_bound, False)

	def test_form_is_bound(self):
		data = {
			'username': self.user.email,
			'password': self.user.password
		}
		self.form = LoginAuthenticationForm(data=data)
		self.assertIs(self.form.is_bound, True)