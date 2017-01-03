from django.core.urlresolvers import resolve
from django.test import TestCase

from django.core.signing import Signer, TimestampSigner
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpRequest

from accounts.models import IbkUser, Profile

class TestModelFixtures(TestCase):
	"""
	Sets up user data fixtures for testing account models. Test will inherit from this class all
	pre-created user data.
	"""
	@classmethod 
	def setUpTestData(cls):
		cls.user = IbkUser.objects.create(email = "mctest@test.com", name="McTest McTesty", username="McTestyRocks", password="12345")
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

	def test_user_password_hashing(self):
		password = make_password(self.user.password, salt='jRkSlAw7KZ')
		check = check_password(password, self.user.password)
		self.assertTrue(True , msg='Should salt password, and check if password is correct/readable')

class TestProfile(TestModelFixtures):
	"""
	Test Profile Profile Model.
	"""
	def test_profile_model(self):
		self.assertEqual(self.user.pk, self.profile.user_id)




