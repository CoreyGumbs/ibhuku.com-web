#!/usr/bin/env python
from django.test import TestCase, Client


from accounts.models import IbkUser, Profile
from profiles.forms import ProfileAvatarUploadForm


class TestDataFixture(TestCase):
    """
    Sets up user data fixtures for testing.
    """
    def setUp(self):
        self.client = Client()
        self.av_upload =  ProfileAvatarUploadForm()

    @classmethod 
    def setUpTestData(cls):
        cls.user = IbkUser.objects.create_user(email = "mctest@test.com", name="McTestMcTesty", username="McTestyRocks", password="password12345")
        cls.data = {
            'name': cls.user.name,
        }

class TestProfileAvatarUploadForm(TestDataFixture):
    """
    Test Profile avatar upload form.
    """

    def test_profile_avatar_upload_form_is_not_bound(self):
        self.assertEqual(self.av_upload.is_bound, False)

    def test_profile_avatar_upload_form_is_bound(self):
        self.av_upload = ProfileAvatarUploadForm(data={})
        self.assertEqual(self.av_upload.is_bound, True)

    def test_profile_avatar_upload_form_is_valid(self):
        self.av_upload = ProfileAvatarUploadForm(data=self.data)
        self.assertIs(self.av_upload.is_valid(), True)

    def test_profile_avatar_upload_from_is_not_valid(self):
        self.assertIs(self.av_upload.is_valid(), False)

    def test_profile_avatar_upload_form_errors(self):
        pass