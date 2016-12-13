from django.core.urlresolvers import resolve
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from accounts.models import IbkUser
from accounts.views import index


# Create your tests here.

#Model Test for IbkUser account information is actually in database/model
class IbkUserAccountTest(TestCase):
	def setUp(self):
		IbkUser.objects.create(email = "mctest@test.com", first_name="McTest", password="12345")

	def test_string_representation(self):
		name = IbkUser(first_name='McTest')
		self.assertEqual('McTest', name.first_name )

	def test_IbkUser_email_created(self):
		name = IbkUser.objects.get(first_name="McTest")
		self.assertIn('mctest@test.com', name.email)

	def test_IbkUser_date_joined(self):
		name = IbkUser.objects.get(first_name="McTest")
		self.assertTrue(name.date_joined, True)

	def test_verbose_name_plural(self):
		self.assertEqual(str(IbkUser._meta.verbose_name_plural), 'ibk users')

	def test_get_full_name(self):
		name = IbkUser(first_name='admin')
		self.assertEqual('admin', name.get_full_name())

	def test_get_short_name(self):
		name = IbkUser(first_name='admin')
		self.assertEqual('admin', name.get_short_name())

#IbkUser Profile creations Test
class IbkUserProfileCreated(TestCase):
	def setUp(self):
		IbkUser.objects.create(email = "mctest@test.com", first_name="McTest", password="12345")

	def test_IbkUser_creation(self):
		name = IbkUser.objects.get(first_name="McTest")
		self.assertIn('mctest@test.com', name.email)

	def test_profile_creation(self):
		name = IbkUser.objects.get(first_name="McTest")
		name.profile.bio = 'test this profile'
		name.profile.location = 'new york'
		name.save()
		self.assertEqual('test this profile', name.profile.bio)
		self.assertEqual('new york', name.profile.location)
		
#Test to see if app url '../accounts/' is responding
class IbkUserAccountsIndexPageTest(TestCase):
	def test_root_url_status_code_to_index_page_view(self):
		response = self.client.get('/accounts/')
		self.assertEqual(response.status_code, 200)

	def test_resolve_root_url_resolves_to_index_view(self):
		found = resolve('/accounts/')
		self.assertEqual(found.func, index)


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

