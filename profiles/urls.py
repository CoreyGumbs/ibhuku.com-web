from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from .views import ProfileLogin

urlpatterns = [
	url(r'^login/$', ProfileLogin, name='login'),
]	