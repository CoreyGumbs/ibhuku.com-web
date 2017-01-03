from django.conf.urls import include, url
from django.contrib.auth import views as auth_views


from profiles.views import profile_index, ProfileLogin, ProfileDashboard

urlpatterns = [
	url(r'^$', profile_index.as_view() ,name='index'),
	url(r'^(?P<pk>[0-9]+)/$', ProfileDashboard, name='dashboard'),
	url(r'^login/$', ProfileLogin, name='login'),
]	