from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import check_password
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.urlresolvers import reverse


from accounts.models import IbkUser, Profile
from auths.forms import LoginAuthenticationForm, AccountRecoveryForm, UserPasswordResetForm
# Create your tests here.
class TestDataFixture(TestCase):
	"""
	Sets up user data fixtures for testing.
	"""
	def setUp(self):
		self.client = Client()
		self.form = LoginAuthenticationForm()
		self.recovery = AccountRecoveryForm()

	@classmethod 
	def setUpTestData(cls):
		cls.user = IbkUser.objects.create_user(email = "mctest@test.com", name="McTest McTesty", username="McTestyRocks", password="password12345")
		cls.data = {
			'username': cls.user.email,
			'password': cls.user.password
		}
		cls.user_token = default_token_generator.make_token(cls.user)
		cls.uid = urlsafe_base64_encode(force_bytes(cls.user.pk))
		cls.reset = UserPasswordResetForm(cls.user)

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
		form = LoginAuthenticationForm(data={'username':'mctest@test.com', 'password': 'password12345'})
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

class TestAccountRecoverForm(TestDataFixture):
	"""
	Test Account Recovery Form
	"""
	def test_recover_form_is_un_bound(self):
		self.assertIs(self.recovery.is_bound, False)

	def test_recover_form_is_bound(self):
		self.recovery = AccountRecoveryForm(data={'email': self.user.email})
		self.assertIs(self.recovery.is_bound, True)

	def test_recover_form_is_not_valid(self):
		self.recovery = AccountRecoveryForm(data={})
		self.assertIs(self.recovery.is_valid(), False)

	def test_recover_form_is_valid(self):
		self.recovery = AccountRecoveryForm(data={'email': self.user.email})
		self.assertIs(self.recovery.is_valid(), True)

	def test_recover_form_errors(self):
		response = self.client.post('/auths/recover/', {'email': ''})
		self.assertFormError(response, 'form', 'email', ['This field is required.'])

	def test_post_email_validation(self):
		response = self.client.post('/auths/recover/', {'email': 'test@testing'})
		self.assertFormError(response, 'form', 'email', ['Enter a valid email address.'])

	def test_recover_form_email_validation(self):
		self.recoveryform = AccountRecoveryForm(data={'email': 'test@testing'})
		self.assertEqual(self.recoveryform.errors, {'email': ['Enter a valid email address.']})

	def test_recover_form_email_cleaning_valid(self):
		self.recoveryform = AccountRecoveryForm(data={'email': self.user.email})
		self.assertTrue(self.recoveryform.is_valid())
		self.assertEqual(self.recoveryform.clean(), {'email': self.user.email})

class TestPasswordResetForm(TestDataFixture):
	"""
	Test Password Reset Form
	"""
	def test_reset_password_is_un_bound_and_not_valid(self):
		self.assertIs(self.reset.is_bound, False)
		self.assertIs(self.reset.is_valid(), False)

	def test_reset_password_is_bound_and_valid(self):
		self.reset = UserPasswordResetForm(self.user, data={'new_password': 'testpassword', 'confrim_password': 'testpassword'})
		self.assertIs(self.reset.is_bound, True)
		self.assertIs(self.reset.is_valid(), True)

	def test_reset_form_errors(self):
		self.reset = UserPasswordResetForm(self.user, data={'new_password': 'RussianDressing', 'confrim_password': 'RussianRoulette'})
		self.assertEqual(self.reset.errors, {'__all__': ["The two password fields didn't match."]})

	def test_reset_form_password_validation(self):
		self.reset = UserPasswordResetForm(self.user, data={'new_password': 'testpassword', 'confrim_password': 'testpassword'})
		self.assertTrue(self.reset.is_valid())
		self.assertEqual(self.reset.clean(), {'new_password': 'testpassword', 'confrim_password': 'testpassword'})

	def test_reset_password_save(self):
		self.reset = UserPasswordResetForm(self.user, data={'new_password': 'testpassword', 'confrim_password': 'testpassword'})
		self.assertTrue(self.reset.is_valid())
		self.reset.save()
		self.assertTrue(check_password('testpassword', self.user.password))
		
		#test to see if new password is the same as old password and returns error if true
		self.reset = UserPasswordResetForm(self.user, data={'new_password': 'testpassword', 'confrim_password': 'testpassword'})
		self.assertEqual({'__all__': ['There was an error with your password. Please try again.']}, self.reset.errors)
















