from django.test import TestCase, Client
from django.contrib.auth import authenticate

from accounts.accountslib import profile_validation_key, authorized_view_session_check, check_profile_validation_key
from accounts.models import IbkUser, Profile
from ..forms import LoginForm

class TestDataFixture(TestCase):
	def setUp(self):
		self.client = Client()
		self.form = LoginForm()
		
class TestLogInForm(TestCase):
	"""
	Test of the Accounts/Profile Login Form.
	"""
	def test_login_form_is_not_valid(self):
		form = LoginForm(data={})
		self.assertIs(form.is_valid(), False, msg='Should return False is errors appear/no data passed')
		self.assertIn('username', form.errors, msg='Returns email error if no email provided')

	def test_accounts_login_form_is_valid(self):
		data = {'username': 'coreygumbs@gmail.com', 'password': 'password12345'}
		form = LoginForm(data=data) 
		print(form.is_valid())
		print(form.errors)
		self.assertIs(form.is_bound, True, msg='Returns True if form is bound by data')
		self.assertIs(form.is_valid(), True, msg='Returns True if data passed through form.')
		self.assertEqual(form.cleaned_data['username'], 'testing@test.com', msg='checks cleaned data is equal to input data/kwargs')
		self.assertEqual(form.cleaned_data['password'], 'password12345', msg='checks cleaned data is equal to input data/kwargs')




