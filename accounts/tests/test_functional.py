from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from accounts.models import IbkUser

class UserCreateAccountTest(StaticLiveServerTestCase):
	"""
	Functional Test of User Account Creation/Sign-Up.
	"""
	@classmethod
	def setUpClass(cls):
		cls.browser = webdriver.Chrome('/usr/local/bin/chromedriver')
		super(UserCreateAccountTest, cls).setUpClass()

	@classmethod
	def tearDownClass(cls):
		cls.browser.quit()
		super(UserCreateAccountTest, cls).tearDownClass()

	def test_user_create_account(self):
		#TestyMcTesty is a history researcher and avid reader
		#He is told by an associate of a site that he can use as a tool to help him organize his reading and research
		#Interested, TestyMcTesty decides to check it out. 
		self.browser.get('{}{}'.format(self.live_server_url, '/accounts/'))

		#He notices he is on the user sign-up page via the page title.
		self.assertIn('Sign-Up!', self.browser.title)

		#There is a form header that informs McTesty of what it is
		form_header = self.browser.find_element_by_tag_name('h2').text
		self.assertEqual('Create Account', form_header)

		#McTesty says "what the heck".
		#He decides to fill out the form. He sees the form has 3 fields, they are:
		#Name (His)
		user_name = self.browser.find_element_by_name('name')
		self.assertIn(user_name.get_attribute('placeholder'), 'Name')
		#email
		user_email = self.browser.find_element_by_name('email')
		self.assertIn(user_email.get_attribute('placeholder'), 'Email')
		#password
		user_password = self.browser.find_element_by_name('password')
		self.assertIn(user_password.get_attribute('placeholder'), 'Password')

		#McTesty Enters his information
		user_name.send_keys('Testy McTesty')
		user_email.send_keys('Mctesty@testy.com')
		user_password.send_keys('password12345')

		#McTesty sends the data.
		self.browser.find_element_by_id('submit-id-submit').click()

		#McTesty recieves a confirmation screen that confirms his registration.
		self.assertIn('Activation Link Emailed',self.browser.title)
		email_sent_header = self.browser.find_element_by_tag_name('h3').text
		self.assertEqual('Your Activation Email Is On The Way.', email_sent_header)





