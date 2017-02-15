#!/usr/bin/env python
import tempfile
from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse


from accounts.models import IbkUser, Profile
from profiles.views import ProfileAvatarUploadView
from profiles.forms import ProfileAvatarUploadForm

class TestDataFixtures(TestCase):
    """
    Data for running of tests.
    """
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        cls.user = IbkUser.objects.create_user(email = "mctest@test.com", name="McTestMcTesty", username="McTestyRocks", password="password12345")
        cls.profile = Profile.objects.get(user_id=cls.user.id)

class TestProfileDashboard(TestDataFixtures):
    """
    Test of the Profile Dashboard View.
    """
    def test_profile_dashboard_url(self):
        login = self.client.login(username=self.user.email, password='password12345')
        response = self.client.get(reverse('profile:dashboard',kwargs={'name': self.user.name}))
        self.assertEqual(response.status_code, 200)

    def test_profile_dashboard_view(self):
        login = self.client.login(username=self.user.email, password='password12345')
        response = self.client.get(reverse('profile:dashboard', kwargs={'name': self.user.name}))
        self.assertEqual(response.resolver_match.func.__name__, 'ProfileDashboardView')

    def test_profile_dashboard_view_kwargs(self):
        login = self.client.login(username=self.user.email, password='password12345')
        response = self.client.get(reverse('profile:dashboard', kwargs={'name': self.user.name}))
        self.assertEqual(response.resolver_match.kwargs, {'name':self.user.name})

    def test_profile_dashboard_html(self):
        login = self.client.login(username=self.user.email, password='password12345')
        response = self.client.get(reverse('profile:dashboard', kwargs={'name': self.user.name}))
        html = response.content.decode('utf8')
        self.assertIn(self.user.name, html)

    def test_profile_dashboard_template(self):
        login = self.client.login(username=self.user.email, password='password12345')
        response = self.client.get(reverse('profile:dashboard', kwargs={'name': self.user.name}))
        self.assertTemplateUsed(response, 'profiles/profile_dashboard.html')

    def test_profile_dashboard_template_context(self):
        login = self.client.login(username=self.user.email, password='password12345')
        response = self.client.get(reverse('profile:dashboard', kwargs={'name': self.user.name}))
        self.assertEqual(response.context['user'].name, 'McTestMcTesty')


class TestAvatarUploadView(TestDataFixtures):
    """
    Test of the Avatar Upload View.
    """

    def test_avatar_upload_view(self):
        login = self.client.login(username=self.user.email, password='password12345')
        response = self.client.post(reverse('profile:avatar-upload',kwargs={'name': self.user.name}))
        self.assertEqual(response.resolver_match.func.__name__, 'ProfileAvatarUploadView')

    def test_avatar_upload_view_kwargs(self):
        login = self.client.login(username=self.user.email, password='password12345')
        response = self.client.post(reverse('profile:avatar-upload', kwargs={'name': self.user.name}))
        self.assertEqual(response.resolver_match.kwargs, {'name':self.user.name})

    def test_avatar_upload_form_context_on_dashboard_template(self):
        login = self.client.login(username=self.user.email, password='password12345')
        response = self.client.get(reverse('profile:dashboard', kwargs={'name': self.user.name}))
        html = response.content.decode('utf8')
        self.assertIn('avatar', html)

    def test_avatar_upload_view_redirection(self): 
        login = self.client.login(username=self.user.email, password='password12345')
        response = self.client.post(reverse('profile:avatar-upload',kwargs={'name': self.user.name}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/profile/McTestMcTesty')

    def test_avatar_upload(self):
        temp_img = tempfile.NamedTemporaryFile()
        login = self.client.login(username=self.user.email, password='password12345')
        response = self.client.put(reverse('profile:avatar-upload',kwargs={'name': self.user.name}))
       












