from django.conf.urls import include, url

from profiles.views import ProfileDashboardView, ProfileAvatarUploadView

urlpatterns = [
	url(r'^(?P<name>[\w.@+-]+)$', ProfileDashboardView , name='dashboard'),
	url(r'^(?P<name>[\w.@+-]+)/avatar/upload/$', ProfileAvatarUploadView, name='avatar-upload'),
]