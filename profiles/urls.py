from django.conf.urls import include, url

from profiles.views import ProfileDashboardView

urlpatterns = [
	url(r'^$', ProfileDashboardView , name='dashboard'),
]