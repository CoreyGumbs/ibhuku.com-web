#!/usr/bin/env python
from django.test import TestCase, Client

from accounts.models import IbkUser, Profile


class TestDataFixtures(TestCase):
    """
    Data for running of tests.
    """
    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        cls.user = IbkUser.objects.create_user(email = "mctest@test.com", name="McTest McTesty", username="McTestyRocks", password="password12345")
        cls.profile = Profile.objects.get(user_id=self.user.id)


class TestProfileDashboard(TestCase):
    """
    Test of the Profile Dashboard
    """
    def test_profile_dashboard_url(self):
        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, 200)

    def test_profile_dashboard_view(self):
        response = self.client.get('/profiles/')
        self.assertEqual(response.resolver_match.func.__name__, 'ProfileDashboardView')


