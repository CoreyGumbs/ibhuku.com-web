from __future__ import unicode_literals
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage

from .managers import UserManager


def user_directory_path(instance, filename):
	return 'useraccounts/user_{0}/{1}'.format(instance.user_id, filename)

def get_account_valid_link_expire():
	return timezone.now() + timedelta(days=3)

# Create your models here.
class IbkUser(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(_('email'),max_length=255, unique=True)
	name = models.CharField(_('name'), max_length=100, blank=False)
	username = models.CharField(_('username'), max_length=100, blank=True)
	date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
	last_login = models.DateTimeField(_('last login'), auto_now=True)
	is_active =  models.BooleanField(_('active'), default=True)
	is_staff = models.BooleanField(_('staff'), default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name']

	class Meta:
		db_table = 'user_accounts'
		verbose_name = _('user')
		verbose_name_plural = _('users') 

	def get_full_name(self):
		if self.username:
			return self.username
		else:
			return self.name

	def get_short_name(self):
		if self.username:
			return self.username
		else:
			return self.name

	def __unicode__(self):
		if self.username:
			return self.username
		else:
			return self.name

	def __str__(self):
		if self.username:
			return self.username
		else:
			return self.name


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	bio =  models.TextField(_('bio'),max_length=500, blank=True)
	location = models.CharField(_('location'), max_length=50, blank=True)
	avatar = models.ImageField(upload_to=user_directory_path, default='default_avatar.jpg',  null=True, blank=True) 
	verified = models.BooleanField(_('verified'), default=False)
	verify_key = models.CharField(_('key'), max_length=250, blank=False)
	expire_date = models.DateTimeField(_('expire date'), default=get_account_valid_link_expire)
	last_login = models.DateTimeField(_('last login'), auto_now=True) 

	class Meta:
		db_table = 'user_profiles'
		verbose_name = _('profile')
		verbose_name_plural = _('profiles')

	def __unicode__(self):
		return self.user.get_full_name()

	def __str__(self):
		return self.user.get_full_name()

