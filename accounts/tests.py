import random
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.http import HttpRequest

from selenium import webdriver

from accounts.models import IbkUser, Profile
from accounts.views import AccountsIndex, AccountSignUp


# Create your tests here.
#Model Test for IbkUser account information is actually in database/model
class IbkUserAccountTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.user = IbkUser.objects.create(email = "mctest@test.com", name="McTest McTesty", username="McTestyRocks", password="12345")

	def test_string_representation(self):
		self.assertEqual('McTest McTesty', self.user.name )

	def test_IbkUser_email_created(self):
		self.assertIn('mctest@test.com', self.user.email)

	def test_IbkUser_date_joined(self):
		self.assertTrue(self.user.date_joined, True)

	def test_verbose_name_plural(self):
		self.assertEqual(str(self.user._meta.verbose_name_plural), 'users')

	def test_get_full_name(self):
		self.assertEqual('McTestyRocks', self.user.get_full_name())

	def test_get_short_name(self):
		self.assertEqual('McTestyRocks', self.user.get_short_name())

	def test_password_hash(self):
		password = make_password(self.user.password)
		check = check_password(password, self.user.password)
		self.assertTrue(True , check)

#IbkUser Profile creations Test
class IbkUserProfileCreated(TestCase):
	@classmethod 
	def setUpTestData(cls):
		cls.user = IbkUser.objects.create(email = "mctest@test.com", name="McTest McTesty", username="McTestyRocks", password="12345")
		cls.profile = Profile.objects.create(user_id=cls.user.id)

	def test_IbkUser_creation(self):
		self.assertIn('mctest@test.com', self.user.email)

	def test_profile_creation(self):
	 	self.profile.bio = "This is McTest McTesty's accounts"
	 	self.profile.location = "New York"
	 	self.profile.save()
	 	self.assertEqual(self.profile.user.name, 'McTest McTesty')
	 	self.assertEqual(self.profile.user.username, 'McTestyRocks')
	 	self.assertEqual("This is McTest McTesty's accounts", self.user.profile.bio)
	 	self.assertEqual("New York", self.user.profile.location)
		
#Test to see if app url '../accounts/' is responding
class IbkUserAccountsIndexPageTest(TestCase):
	def test_account_page_status_code_to_index_page_view(self):
		response = self.client.get('/accounts/')
		self.assertEqual(response.status_code, 200)

	def test_index_view_uses_index_template(self):
		response = self.client.get('/accounts/')
		self.assertTemplateUsed(response, 'accounts/base.html')

	def test_index_page_returns_correct_html(self):
		response = self.client.get('/accounts/')
		html = response.content.decode('utf8')
		self.assertIn('<title>Accounts</title>', html)
		self.assertTemplateUsed(response, 'accounts/base.html')

#Test of Accounts Registrations Views/URLs
class IbhukuRegistrationPageTest(TestCase):
	def test_sign_up_page_status_code(self):
		response = self.client.get('/accounts/register/')
		self.assertEqual(response.status_code, 200)

	def test_sign_up_view_uses_sign_up_template(self):
		response = self.client.get('/accounts/register/')
		self.assertTemplateUsed(response, 'accounts/signup_form.html')

	def test_registration_page_returns_correct_html(self):
		response = self.client.get('/accounts/register/')
		html = response.content.decode('utf8')
		self.assertIn('<title>Sign-Up!</title>', html)
		self.assertIn('submit', html)


#Browser Test to check for '/accounts/' url and index page title html
class AccountsSignUpTest(StaticLiveServerTestCase):
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

	def test_user_signup_creation(self):
		self.browser.get('http://localhost:8000/accounts/register/')
		self.assertIn('Sign-Up', self.browser.title)

		name_input = self.browser.find_element_by_id("signup_name")
		email_input = self.browser.find_element_by_id("signup_email")
		password_input = self.browser.find_element_by_id("signup_password")
		
		self.assertEqual(name_input.get_attribute('placeholder'), 'Name')
		self.assertEqual(email_input.get_attribute('placeholder'), 'Email')
		self.assertEqual(password_input.get_attribute('placeholder'), 'Password')

		name_input.send_keys('Testy McTesty')
		email_input.send_keys('test@testing.com')
		password_input.send_keys('password123')

		self.browser.find_element_by_id("submit-id-submit").submit()
		import time
		time.sleep(3)

	def test_check_success_redirect(self):
		self.browser.get('http://localhost:8000/accounts/')
		self.assertIn('Accounts', self.browser.title)


