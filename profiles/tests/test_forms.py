#!/usr/bin/env python
import tempfile
from django.test import TestCase, Client, RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile


from accounts.models import IbkUser, Profile
from profiles.forms import ProfileAvatarUploadForm


class TestDataFixture(TestCase):
    """
    Sets up user data fixtures for testing.
    """
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.av_upload =  ProfileAvatarUploadForm()

    @classmethod 
    def setUpTestData(cls):
        cls.user = IbkUser.objects.create_user(email = "mctest@test.com", name="McTestMcTesty", username="McTestyRocks", password="password12345")
        cls.profile = Profile.objects.get(user_id=cls.user.id)
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
        self.av_upload = ProfileAvatarUploadForm(data={'avatar': 'fake_img.jpg'})
        self.assertIs(self.av_upload.is_valid(), True)

    def test_profile_avatar_upload_from_is_not_valid(self):
        self.assertIs(self.av_upload.is_valid(), False)

    def test_profile_avatar_upload_form_passes_data(self):
        pass

