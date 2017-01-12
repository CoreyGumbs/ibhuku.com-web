from django.test import TestCase, Client
from .. import forms


class TestIbhukuSignUpForm(TestCase):
	"""
	Test of the Ibhuku Sign-up/Registration Form. 
	"""
	def test_form_without_data_is__not_valid(self):
		form = forms.IbkUserSignUpForm(data={})
		self.assertFalse(form.is_valid(), msg='Returns false if form invalid/no data')
		self.assertIn('name', form.errors, msg='Looks for form fields in error fields')

	def test_form_with_data_is_valid(self):
		data ={
			'name': 'Testy McTesty',
			'email': 'testy@testing.com',
			'password': 'password1235'
		}
		form = forms.IbkUserSignUpForm(data=data)
		self.assertTrue(form.is_valid(), msg='Returns true if form valid')

	def test_form_password_invalid_length(self):
		data ={'password': 'pass',}
		form = forms.IbkUserSignUpForm(data=data)
		self.assertIn('password', form.errors, msg='Returns error on password if too short.')
