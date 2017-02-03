#!/usr/bin/env python
from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password

from accounts.models import IbkUser, Profile

class TestModelFixtures(TestCase):
	"""
	Sets up user data fixtures for testing account models. Test will inherit from this class all
	pre-created user data.
	"""
	@classmethod 
	def setUpTestData(cls):
		cls.user = IbkUser.objects.create(email = "mctest@test.com", name="McTest McTesty", username="McTestyRocks", password="12345")
		cls.user.password = make_password(cls.user.password, salt='jRkSlAw7KZ')
		cls.user.save()
		cls.profile = Profile.objects.get(user_id=cls.user.id)

class TestIbkUser(TestModelFixtures):
	"""
	Test IbkUser Abstract Base Model for User database table.
	"""
	def test_ibk_user_model(self):
		self.assertEqual(self.user.pk, 1, msg='Returns true if created User id/ok equals specified id/pk number')

	def test_string_representation(self):
		self.assertEqual(self.user.username, self.user.__str__(), msg='Should return __str__ representation')

	def test_unicode_string_representation(self):
		self.assertEqual(self.user.username, self.user.__unicode__(), msg='Should return __unicode__ representation')

	def test_user_email_created(self):
		self.assertIn('mctest@test.com', self.user.email, msg='Should return user email')

	def test_user_date_joined(self):
		self.assertTrue(self.user.date_joined, msg='Should return True if date was saved')

	def test_verbose_name_plural(self):
		self.assertEqual(str(self.user._meta.verbose_name_plural), 'users', msg='Should return database table verbose name found in Meta class on model')

	def test_get_full_name(self):
		self.assertEqual('McTestyRocks', self.user.get_full_name(), msg='Should return the get_full_name() on AbstractBaseUser model')

	def test_get_short_name(self):
		self.assertEqual('McTestyRocks', self.user.get_short_name(), msg='Should return the get_short_name() on AbstractBaseUser model')

	def test_check_user_password(self):
		check_pass = check_password('12345', self.user.password)
		self.assertTrue(check_pass, msg='Should return True if password and hashed password equal.')

class TestProfile(TestModelFixtures):
	"""
	Test Profile Profile Model creation and save.
	"""
	def test_profile_model(self):
		self.assertEqual(self.user.pk, self.profile.user_id)

	def test_profile_save(self):
		self.profile.bio = "This is McTest McTesty's accounts"
		self.profile.location = "New York"
		self.profile.save()
		self.assertEqual("This is McTest McTesty's accounts", self.profile.bio, msg='should return saved profile bio data')
		self.assertEqual("New York", self.profile.location, msg='Should return saved profile location data')

	def test_profile_one_to_one_ibk_user_relationship(self):
		self.assertEqual(self.profile.user.name, 'McTest McTesty', msg='Should return User model name filed data from OneToOne relation')
		self.assertEqual(self.profile.user.username, 'McTestyRocks', msg='Should return User model username field data from OneToOne relation')

	def test_string_representation(self):
		self.assertEqual(self.user.username, self.profile.__str__(), msg='Should return __str__ representation')

	def test_unicode_string_representation(self):
		self.assertEqual(self.user.username, self.profile.__unicode__(), msg='Should return __unicode__ representation')




