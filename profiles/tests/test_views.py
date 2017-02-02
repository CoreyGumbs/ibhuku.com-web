#!/usr/bin/env python
from django.test import TestCase, Client
from django.core.urlresolvers import reverse


from accounts.models import IbkUser, Profile


class TestDataFixtures(TestCase):
    """
    Data for running of tests.
    """
    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        cls.user = IbkUser.objects.create_user(email = "mctest@test.com", name="McTestMcTesty", username="McTestyRocks", password="password12345")
        cls.profile = Profile.objects.get(user_id=cls.user.id)

class TestProfileDashboard(TestDataFixtures):
    """
    Test of the Profile Dashboard
    """
    def test_profile_dashboard_url(self):
        response = self.client.get(reverse('profile:dashboard', kwargs={'name': self.user.name}))
        self.assertEqual(response.status_code, 200)

    def test_profile_dashboard_view(self):
        response = self.client.get(reverse('profile:dashboard', kwargs={'name': self.user.name}))
        self.assertEqual(response.resolver_match.func.__name__, 'ProfileDashboardView')

    def test_profile_dashboard_html(self):
        response = self.client.get(reverse('profile:dashboard', kwargs={'name': self.user.name}))
        html = response.content.decode('utf8')
        self.assertIn('<title>Profile Dashboard</title>', html)

    def test_profile_dashboard_template(self):
        response = self.client.get(reverse('profile:dashboard', kwargs={'name': self.user.name}))
        self.assertTemplateUsed(response, 'profiles/profile_dashboard.html')


