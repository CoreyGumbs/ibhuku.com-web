from django.test import TestCase


from ..forms import LoginAuthenticationForm
# Create your tests here.

class TestLoginAuthenticationForm(TestCase):
	"""
	Test Ibhuku Account Login Form
	"""
	def setUp(self):
		self.form = LoginAuthenticationForm()

	def test_form_is_bound(self):
		self.assertIs(self.form.is_bound, False)
