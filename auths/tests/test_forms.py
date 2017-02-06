#!/usr/bin/env python
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
		self.assertIs(self.form.is_bound, False, msg='Should return False if form is unbound')

	def test_form_is_bound(self):
		self.form = LoginAuthenticationForm(data=self.data)
		self.assertIs(self.form.is_bound, True, msg='Should return True if form is bound')

	def test_form_not_valid(self):
		self.form = LoginAuthenticationForm(data={})
		self.assertIs(self.form.is_valid(), False, msg='Should return False is form is not valid')

	def test_form_is_valid(self):
		form = LoginAuthenticationForm(data={'username':'mctest@test.com', 'password': 'password12345'})
		self.assertIs(form.is_valid(), True, msg='Should return True if form valid')
		self.assertEqual(form.data['username'], self.user.email, msg='Entered form data should equal user email')

	def test_form_html(self):
		response = self.client.get('/auths/login/')
		html = response.content.decode('utf8')
		self.assertIn(
			'<input class="textinput textInput form-control" id="login_password" name="password" type="password" required />', 
			html, 
			msg='True if string/elements found in html.'
			)

	def test_form_errors(self):
		response = self.client.post('/auths/login/', {'username': '', 'password': ''})
		self.assertFormError(response, 'form', 'username', ['This field is required.'], msg_prefix='Should return username field error message')
		self.assertFormError(response, 'form', 'password', ['This field is required.'], msg_prefix='Should return password field error message')

	def test_form_incorrect_account_errors(self):
		response = self.client.post('/auths/login/', {'username': 'testing@whatif.com', 'password': 'runforestrun'})
		self.assertFormError(response, 'form', None, 'The username or password you entered are incorrect.', msg_prefix='Should return wrong account error message')

class TestAccountRecoverForm(TestDataFixture):
	"""
	Test Account Recovery Form
	"""
	def test_recover_form_is_un_bound(self):
		self.assertIs(self.recovery.is_bound, False, msg='Should return False if form is unbound.')

	def test_recover_form_is_bound(self):
		self.recovery = AccountRecoveryForm(data={'email': self.user.email})
		self.assertIs(self.recovery.is_bound, True, msg='Should return True if form is bound.')

	def test_recover_form_is_not_valid(self):
		self.recovery = AccountRecoveryForm(data={})
		self.assertIs(self.recovery.is_valid(), False, msg='Should return False is form is not valid.')

	def test_recover_form_is_valid(self):
		self.recovery = AccountRecoveryForm(data={'email': self.user.email})
		self.assertIs(self.recovery.is_valid(), True, msg='Should return True if form is valid.')

	def test_recover_form_errors(self):
		response = self.client.post('/auths/recover/', {'email': ''})
		self.assertFormError(response, 'form', 'email', ['This field is required.'], msg_prefix='Should return email field error.')

	def test_post_email_validation(self):
		response = self.client.post('/auths/recover/', {'email': 'test@testing'})
		self.assertFormError(response, 'form', 'email', ['Enter a valid email address.'], msg_prefix='Should return invalid email error.')

	def test_recover_form_email_validation(self):
		self.recoveryform = AccountRecoveryForm(data={'email': 'test@testing'})
		self.assertEqual(self.recoveryform.errors, {'email': ['Enter a valid email address.']}, msg='Should return invalid email error.')

	def test_recover_form_email_cleaning_valid(self):
		self.recoveryform = AccountRecoveryForm(data={'email': self.user.email})
		self.assertTrue(self.recoveryform.is_valid(), msg='Should return True if form is valid.')
		self.assertEqual(self.recoveryform.clean(), {'email': self.user.email}, msg='Email should equal cleaned data from form.')

class TestPasswordResetForm(TestDataFixture):
	"""
	Test Password Reset Form
	"""
	def test_reset_password_is_un_bound_and_not_valid(self):
		self.assertIs(self.reset.is_bound, False, msg='Should return False if form is unbound.')
		self.assertIs(self.reset.is_valid(), False, msg='Should return Fasle if form is not valid')

	def test_reset_password_is_bound_and_valid(self):
		self.reset = UserPasswordResetForm(self.user, data={'new_password': 'testpassword', 'confrim_password': 'testpassword'})
		self.assertIs(self.reset.is_bound, True, msg='Should return True if form is bound.')
		self.assertIs(self.reset.is_valid(), True, msg='Should return True if form valid')

	def test_reset_form_errors(self):
		self.reset = UserPasswordResetForm(self.user, data={'new_password': 'RussianDressing', 'confrim_password': 'RussianRoulette'})
		self.assertEqual(self.reset.errors, {'__all__': ["The two password fields didn't match."]}, msg='Should return fields dont match error.')

	def test_reset_form_password_validation(self):
		self.reset = UserPasswordResetForm(self.user, data={'new_password': 'testpassword', 'confrim_password': 'testpassword'})
		#have to run this assertion in order to trigger the clean() method.
		self.assertTrue(self.reset.is_valid(), msg='Should return True if form valid.')
		self.assertEqual(
			self.reset.clean(), 
			{'new_password': 'testpassword', 'confrim_password': 'testpassword'}, 
			msg='Should return password field data in clean()'
			)

	def test_reset_password_save(self):
		self.reset = UserPasswordResetForm(self.user, data={'new_password': 'testpassword', 'confrim_password': 'testpassword'})
		#have to run this assertion in order to trigger the clean() method.
		self.assertTrue(self.reset.is_valid(), msg='Should return True if form valid')
		self.reset.save()
		self.assertTrue(check_password('testpassword', self.user.password), msg='Returns True if new password saved to user.')
		
		#test to see if new password is the same as old password and returns error if true
		self.reset = UserPasswordResetForm(self.user, data={'new_password': 'testpassword', 'confrim_password': 'testpassword'})
		self.assertEqual(
			{'__all__': ['There was an error with your password. Please try again.']}, 
			self.reset.errors,
			msg='Should return error if old password = new password.'
			)
















