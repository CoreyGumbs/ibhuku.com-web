from django.contrib.auth.hashers import check_password


from accounts.models import IbkUser

class EmailBackend(object):
	def authenticate(self, email=None, password=None, **kwargs):
		try:
			user = IbkUser.objects.get(email=email)
			if check_password(password, user.password):
				return user
			else:
				return False
		except IbkUser.DoesNotExist:
			return "User does not exist"

	def get_user(self, user_id):
		try:
			return IbkUser.objects.get(pk=user_id)
		except IbkUser.DoesNotExist:
			return None