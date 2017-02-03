from django.test import TestCase, Client

from accounts.forms import IbkUserSignUpForm, ResetActivationLinkForm
from accounts.models import IbkUser, Profile

class TestFixtures(TestCase):
	"""
	Set up data for Tests.
	"""
	def setUp(self):
		self.client = Client()
		self.signup = IbkUserSignUpForm()
		self.reset = ResetActivationLinkForm()

	@classmethod
	def setUpTestData(cls):
		cls.user = IbkUser.objects.create_user(email = "mctest@test.com", name="McTest McTesty", username="McTestyRocks", password="password12345")
		cls.data = {
			'name': cls.user.name,
			'username': cls.user.email,
			'password': cls.user.password
		}

class TestSignUpForm(TestFixtures):
	"""
	Test user account sign-up/creation form.
	"""
	def test_form_is_not_bound(self):
		self.assertIs(self.signup.is_bound, False, msg='Returns False is form is not bound')

	def test_form_is_bound(self):
		self.signup = IbkUserSignUpForm(data=self.data)
		self.assertIs(self.signup.is_bound, True, msg='Returns True if form is bound')

	def test_form_not_valid(self):
		self.signup = IbkUserSignUpForm(data={})
		self.assertIs(self.signup.is_valid(), False, msg='Returns False if not valid')

	def test_form_is_valid(self):
		form = IbkUserSignUpForm(data={'name': 'McTest McTesty', 'email': 'test@test.com', 'password': 'password12345'})
		self.assertIs(form.is_valid(), True, msg='Returns True if form is_valid')

	def test_form_html(self):
		response = self.client.get('/accounts/register/')
		html = response.content.decode('utf-8')
		self.assertIn( 
			'<input class="textinput textInput form-control" id="signup_name" maxlength="100" name="name" placeholder="Name" type="text" required />',
			html,
			msg='Returns True if form input is found in html/form'
			)
	def test_form_errors(self):
		response = self.client.post('/accounts/register/', {'name': '', 'email': '', 'password': ''})
		self.assertFormError(response, 'form', 'name', ['This field is required.'], msg_prefix='Should return name field error message')

	def test_form_error_email(self):
		response = self.client.post('/accounts/register/', {'name': 'Test', 'email': 'test@test', 'password': 'password12345'})
		self.assertFormError(response, 'form', 'email', ['Enter a valid email address.'], msg_prefix='Should return email field error message')

	def test_form_error_password(self):
		response = self.client.post('/accounts/register/', {'name': 'Test', 'email': 'test@test', 'password': 'pass'})
		self.assertFormError(response, 'form', 'password', ['Password must be at least 8 characters.'], msg_prefix='Should return email field error message')

class TestResetActivationLinkForm(TestFixtures):
	"""
	Test Reset Activation Link Form.
	"""

	def test_form_is_not_bound(self):
		self.assertIs(self.reset.is_bound, False, msg='Returns False if form is not bound.')

	def test_form_is_bound(self):
		self.reset = ResetActivationLinkForm(data={'email': self.user.email})
		self.assertIs(self.reset.is_bound, True)

	def test_form_is_not_valid(self):
		form = ResetActivationLinkForm()
		self.assertIs(form.is_valid(), False)

	def test_form_is_valid(self):
		form = ResetActivationLinkForm(data={'email': 'test@test.com'})
		self.assertIs(form.is_valid(), True)

	def test_form_html(self):
		response = self.client.get('/accounts/reset/')
		html = response.content.decode('utf-8')
		self.assertIn('', html)

	def test_form_clean(self):
		form = ResetActivationLinkForm(data={'email': 'test@test.com'})
		self.assertIs(form.is_valid(), True)
		self.assertEqual(form.clean(), {'email': 'test@test.com'})

	def test_form_errors(self):
		response = self.client.post('/accounts/reset/', {'email': ''})
		self.assertFormError(response, 'form', 'email', ['This field is required.'], msg_prefix='Should return name field error message')

	def test_form_error_email(self):
		response = self.client.post('/accounts/reset/', {'email': 'test@test'})
		self.assertFormError(response, 'form', 'email', ['Enter a valid email address.'], msg_prefix='Should return email field error message')









