from django.contrib.auth.tokens import PasswordResetTokenGenerator
from accounts.models import IbkUser, Profile

my_user = IbkUser.objects.get(email='coreygumbs@gmail.com')

def make_link_token(email):
	a = PasswordResetTokenGenerator()
	return a.make_token(email)

def check_link_token(user, token):
	a = PasswordResetTokenGenerator()
	checked_token = a.check_token(user, token)
	if checked_token is True:
		print('Token is correct.')
	else:
		print('try again.')


my_token = make_link_token(my_user)
check_my_token =check_link_token(my_user, my_token)

