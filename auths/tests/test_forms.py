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
		cls.data = {
			'email': cls.user.email,
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

	def test_form_not_valid(self):
		self.form = LoginAuthenticationForm(data={})
		self.assertIs(self.form.is_valid(), False)

	def test_form_is_valid(self):
		self.form = LoginAuthenticationForm(data=self.data)
		self.assertIs(self.form.is_valid(), True)

	def test_form_html(self):
		response = self.client.get('/auths/login/')
		html = response.content.decode('utf8')
		self.assertIn('password', html)

	def test_form_errors(self):
		self.form = LoginAuthenticationForm(data={'email': '', 'password': ''})
		self.assertIn('password', self.form.errors)

	def test_form_cleaned_email(self):
		response = self.client.post('/auths/login/', data={'email': 'johndoe@doe.com', 'password': self.user.password})
		self.assertFormError(response, 'form', '', 'The username or password you entered is incorrect.')

	def test_create_account_link(self):
		response = self.client.get('/auths/login/')
