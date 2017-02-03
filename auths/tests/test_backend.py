#!/usr/bin/env python
from django.test import TestCase, Client
from django.contrib.auth import authenticate
from django.conf import settings

from auths.forms import LoginAuthenticationForm
from auths.backend import EmailLoginBackend
from accounts.models import IbkUser, Profile



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

class TestEmailAuthenticationBackEnd(TestDataFixture):
	def test_user_authentication(self):
		backend = EmailLoginBackend()
		my_user = backend.authenticate(email='coreygumbs@gmail.com', password='password')
		
		