from django.test import TestCase, Client
from django.contrib.auth import get_user_model


from accounts.models import IbkUser, Profile
from auths.forms import LoginAuthenticationForm
# Create your tests here.

class TestDataFixture(TestCase):
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
			'username': cls.user.email,
			'password': cls.user.password
		}

class TestLoginAuthenticationForm(TestDataFixture):
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
		form = LoginAuthenticationForm(None, self.data)
		print(form.data['username'])
		print(form.is_valid())
		self.assertIs(form.is_valid(), True)
		self.assertEqual(form.data['username'], self.user.email)

	def test_form_html(self):
		response = self.client.get('/auths/login/')
		html = response.content.decode('utf8')
		self.assertIn('password', html)

	def test_form_errors(self):
		response = self.client.post('/auths/login/', {'username': '', 'password': ''})
		self.assertFormError(response, 'form', 'username', ['This field is required.'])
		self.assertFormError(response, 'form', 'password', ['This field is required.'])

	def test_form_incorrect_account_errors(self):
		response = self.client.post('/auths/login/', {'username': 'testing@whatif.com', 'password': 'runforestrun'})
		self.assertFormError(response, 'form', None, 'Please enter a correct email and password. Note that both fields may be case-sensitive.')

	def test_create_account_link(self):
		response = self.client.get('/auths/login/')
