from django.core.urlresolvers import resolve
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.http import HttpRequest
from selenium import webdriver

from accounts.models import IbkUser, Profile
from accounts.views import index, registration


# Create your tests here.
#Model Test for IbkUser account information is actually in database/model
class IbkUserAccountTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.user = IbkUser.objects.create(email = "mctest@test.com", first_name="McTest", last_name="McTesty", password="12345")

	def test_string_representation(self):
		self.assertEqual('McTest', self.user.first_name )

	def test_IbkUser_email_created(self):
		self.assertIn('mctest@test.com', self.user.email)

	def test_IbkUser_date_joined(self):
		self.assertTrue(self.user.date_joined, True)

	def test_verbose_name_plural(self):
		self.assertEqual(str(self.user._meta.verbose_name_plural), 'users')

	def test_get_full_name(self):
		self.assertEqual('McTest McTesty', self.user.get_full_name())

	def test_get_short_name(self):
		self.assertEqual('McTest M', self.user.get_short_name())

#IbkUser Profile creations Test
class IbkUserProfileCreated(TestCase):
	@classmethod 
	def setUpTestData(cls):
		cls.user = IbkUser.objects.create(email = "mctest@test.com", first_name="McTest", last_name="McTesty", password="12345")
		cls.profile = Profile.objects.create(user_id=cls.user.id)

	def test_IbkUser_creation(self):
		self.assertIn('mctest@test.com', self.user.email)

	def test_profile_creation(self):
	 	self.profile.bio = "This is McTest McTesty's accounts"
	 	self.profile.location = "New York"
	 	self.profile.save()
	 	self.assertEqual(self.profile.user.first_name, 'McTest')
	 	self.assertEqual("This is McTest McTesty's accounts", self.user.profile.bio)
	 	self.assertEqual("New York", self.user.profile.location)
		
#Test to see if app url '../accounts/' is responding
class IbkUserAccountsIndexPageTest(TestCase):
	def test_root_url_status_code_to_index_page_view(self):
		response = self.client.get('/accounts/')
		self.assertEqual(response.status_code, 200)

	def test_uses_index_template(self):
		response = self.client.get('/accounts/')
		self.assertTemplateUsed(response, 'accounts/index.html')

	def test_index_page_returns_correct_html(self):
		response = self.client.get('/accounts/')
		html = response.content.decode('utf8')
		self.assertTrue(html.startswith('<!DOCTYPE html>'))
		self.assertIn('<title>Accounts</title>', html)
		self.assertTrue(html.endswith('</html>'))
		self.assertTemplateUsed(response, 'accounts/index.html')

# class IbhukuRegistrationPageTest(TestCase):
# 	def test_registration_page_status_code(self):
# 		response = self.client.get('/accounts/register/')
# 		self.assertEqual(response.status_code, 200)


#Browser Test to check for '/accounts/' url and index page title html
class AccountsUrlTest(StaticLiveServerTestCase):
	#set up selenium/browser
	def setUp(self):
		#ChromeDriver
		self.browser = webdriver.Chrome('/usr/local/bin/chromedriver')
		self.browser.implicitly_wait(10)

	#tear down browser after testing
	def tearDown(self):
		self.browser.quit()

	def test_get_accounts_url(self):
		self.browser.get('http://localhost:8000/accounts/')
		self.assertIn("Accounts", self.browser.title)
		import time
		time.sleep(5)

