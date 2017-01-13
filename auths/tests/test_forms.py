from django.test import TestCase, Client

from accounts.models import IbkUser, Profile
from auths.forms import LoginAuthenticationForm
# Create your tests here.

class TestData(TestCase):
	"""
	Sets up user data fixtures for testing.
	"""
	def setUp(self):
		self.client = Client()
		self.form = LoginAuthenticationForm()

	@classmethod 
	def setUpTestData(cls):
		cls.user = IbkUser.objects.create(email = "mctest@test.com", name="McTest McTesty", username="McTestyRocks", password="password12345")
		cls.profile = Profile.objects.get(user_id=cls.user.id)
		cls.profile.save()
		cls.data = {
			'username': cls.user.email,
			'password': cls.user.password
		}

class TestLoginAuthenticationForm(TestData):
	"""
	Test Ibhuku Account Login Form
	"""
	def test_form_is_un_bound(self):
		self.assertIs(self.form.is_bound, False)

	def test_form_is_bound(self):
		self.form = LoginAuthenticationForm(data=self.data)
		self.assertIs(self.form.is_bound, True)

	def test_form_is_valid(self):
		self.form = LoginAuthenticationForm(data=self.data)
		print(self.form.errors)
		print(self.form.cleaned_data['password'])
		self.assertIs(self.form.is_valid(), True)
