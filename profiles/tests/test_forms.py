#!/usr/bin/env python
from django.test import TestCase, Client


from accounts.models import IbkUser, Profile
class TestDataFixture(TestCase):
    """
    Sets up user data fixtures for testing.
    """
    def setUp(self):
        self.client = Client()

    @classmethod 
    def setUpTestData(cls):
        cls.user = IbkUser.objects.create_user(email = "mctest@test.com", name="McTestMcTesty", username="McTestyRocks", password="password12345")