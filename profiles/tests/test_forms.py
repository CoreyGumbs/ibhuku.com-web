from django.test import TestCase, Client
from django.contrib.auth import authenticate
from ..forms import AccountLogInForm

from accounts.accountslib import profile_validation_key, authorized_view_session_check, check_profile_validation_key
from accounts.models import IbkUser, Profile

class TestAccountLogInForm(TestCase):
	"""
	Test of the Accounts/Profile Login Form.
	"""
	def test_login_form_is_not_valid(self):
		form = AccountLogInForm(data={})
		self.assertFalse(form.is_valid(), msg='Should return False is errors appear/no data passed')
		self.assertIn('email', form.errors, msg='Returns email error if no email provided')

	def test_accounts_login_form_is_valid(self):
		data = {'email': 'testing@test.com', 'password': 'password12345'}
		form = AccountLogInForm(data=data) 
		self.assertTrue(form.is_bound, msg='Returns True if form is bound by data')
		self.assertTrue(form.is_valid(), msg='Returns True if data passed through form.')
		self.assertEqual(form.cleaned_data['email'], 'testing@test.com', msg='checks cleaned data is equal to input data/kwargs')
		self.assertEqual(form.cleaned_data['password'], 'password12345', msg='checks cleaned data is equal to input data/kwargs')




