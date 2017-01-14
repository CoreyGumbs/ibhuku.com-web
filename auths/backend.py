from django.contrib.auth.hashers import check_password


from accounts.models import IbkUser

class EmailLoginBackend(object):
	def authenticate(self, email='', password=''):
		try:
			user = IbkUser.objects.get(email=email)
			if check_password(password, user.password):
				return user
			else:
				return None
		except IbkUser.DoesNotExist:
			return None

	def get_user(self, user_id):
		try:
			return IbkUser.objects.get(pk=user_id)
		except IbkUser.DoesNotExist:
			return None