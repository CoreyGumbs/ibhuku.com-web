from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import IbkUser, Profile

# Register your models here.

class IbkUserProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False
	verbose_name_plural = 'Profile'
	fk_name = 'user'

class IbkUserAdmin(UserAdmin):
	inlines = (IbkUserProfileInline, )
	list_display = ['id', 'first_name', 'last_name', 'email', 'is_active', 'is_staff','is_superuser', 'date_joined', 'last_login']
	exclude = ['username', ]

	def get_location(self, instance):
		return instance.profile.location

	get_location.short_description = 'Location'

	def get_inline_instances(self, request, obj=None):
		if not obj:
			return list()
		return super(IbkUserAdmin, self).get_inline_instances(request, obj)

#admin.site.register(IbkUser, IbkUserAdmin)