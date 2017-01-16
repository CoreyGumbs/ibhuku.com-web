from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from .views import LoginView

urlpatterns = [
	url(r'^login/$', auth_views.login,{'template_name': 'auths/login.html'}, name='login')
]