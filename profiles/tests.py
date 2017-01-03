import time

from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


from accounts.models import IbkUser, Profile
from profiles.views import ProfileDashboard

# Create your tests here.
class UnAuthorizedProfilesDashboardPageTest(TestCase):
	"""
	Test for unauthorized access to dashboard page via user not being logged in or authenticated
	using @login_required view decorator.
	"""

	def test_profile_page_url(self):
		"""
		Test url '/profile/' returns 200 when is accessed.
		"""
		response = self.client.get('/profiles/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'profiles/login_required.html')

	def test_profile_page_redirect(self):
		"""
		Test access denied page redirects to login page using javascript redirection
		"""
		response = self.client.get('/profiles/')
		self.assertEqual(response.status_code, 200)
		time.sleep(6)
		self.assertRedirects(response, '/profiles/login/', status_code=301, target_status_code=301)

	def test_profile_dashboard_page_pk_parameter_injection(self):
		"""
		Test @login_required decorator redirects url injected <pk> that is not authenticated
		"""
		response = self.client.get('/profiles/{pk}'.format(pk=1), follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertRedirects(response, '/profiles/login/?next=/profiles/1/', status_code=301)

	# def test_profile_dash_board_template(self):
	# 	response = self.client.get('/profiles/')
	# 	html = response.content.decode('utf8')
	# 	self.assertTemplateUsed(response, 'profiles/dashboard.html')
	# 	self.assertIn('<title>Profile Dashboard</title>', html)


class UserProfileTestDataSetUp(TestCase):
	"""
	Sets up user and profile test data for Profiles app.
	Some test will inherit from this class for testing Profiles app views and logic.
	"""
	def setUp(self):
		"""
		Set up Django's RequestFactory() and Client() for HTTP request/response.
		"""
		self.factory = RequestFactory()
		self.client = Client()

	@classmethod
	def setUpTestData(cls):
		"""
		Set up user and user profile data in database. 
		"""
		cls.user = IbkUser.objects.create(email = "johndoe@test.com", name="John Doe", username="JohnnyBread", password="12345")
		cls.profile = Profile.objects.get(user_id=cls.user.id)

	def test_profile_test_data(self):
		self.assertEqual(self.user.name, 'John Doe')
		self.assertEqual(self.profile.user.username, 'JohnnyBread')


class ProfileLoginPageTest(UserProfileTestDataSetUp):
	"""
	Test the Profiles app login view and urls.
	"""
	def test_get_login_url(self):
		"""
		Test that the URL for the login view resolves to the correct view function
		"""
		response = self.client.get('/profiles/login/')
		html = response.content.decode('utf8')
		self.assertEqual(response.status_code, 200)
		self.assertIn('<title>Ibhuku Member Login</title>', html)

	def test_login_page_template(self):
		response = self.client.get('/profiles/login/')
		self.assertTemplateUsed(response, 'log/login.html')

