#!/usr/bin/env python
import tempfile
from django.test import TestCase, Client
from django.core.urlresolvers import reverse


from accounts.models import IbkUser, Profile
from profiles.forms import ProfileAvatarUploadForm

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

    def test_avatar_upload_view_url(self):
        login =  self.client.login(username=self.user.email, password='password12345')
        response = self.client.get(reverse('profile:avatar-upload', kwargs={'name': self.user.name,'pk': self.user.id}))
        self.assertEqual(response.status_code, 200)

    def test_avatar_upload_view(self):
        login = self.client.login(username=self.user.email, password='password12345')
        response = self.client.get(reverse('profile:avatar-upload', kwargs={'name': self.user.name,'pk': self.user.id}))
        self.assertEqual(response.resolver_match.func.__name__, 'ProfileAvatarUploadView')

    def test_avatar_upload_view_kwargs(self):
        login = self.client.login(username=self.user.email, password='password12345')
        response = self.client.get(reverse('profile:avatar-upload', kwargs={'name': self.user.name,'pk': self.user.id}))
        self.assertEqual(response.resolver_match.kwargs, {'pk': '1', 'name': 'McTestMcTesty'})

    def test_avatar_upload_view_html(self):
        login = self.client.login(username=self.user.email, password='password12345')
        response = self.client.get(reverse('profile:avatar-upload', kwargs={'name': self.user.name,'pk': self.user.id}))
        html = response.content.decode('utf8')
        self.assertIn('<title>Upload Profile Picture</title>', html)

    def test_avatar_upload_view_template(self):
        login = self.client.login(username=self.user.email, password='password12345')
        response = self.client.get(reverse('profile:avatar-upload', kwargs={'name': self.user.name,'pk': self.user.id}))
        self.assertTemplateUsed(response, 'profiles/profile_avatar_upload.html')

    def test_avatar_upload_view_template_context(self):
        login = self.client.login(username=self.user.email, password='password12345')
        response = self.client.get(reverse('profile:avatar-upload', kwargs={'name': self.user.name,'pk': self.user.id}))
        self.assertEqual(response.context['profile'].user.name, 'McTestMcTesty')

    def test_avatar_upload_view_default_image_exists(self):
        self.assertEqual(str(self.profile.avatar), '/static/images/gilfoyle.jpg')

    def test_avatar_upload_view_default_image_updated(self):
        login = self.client.login(username=self.user.email, password='password12345')
        response = self.client.get(reverse('profile:avatar-upload', kwargs={'name': self.user.name,'pk': self.user.id}))
        print(self.profile.avatar)   









