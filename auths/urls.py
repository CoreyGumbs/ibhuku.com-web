from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from .views import LoginView

from .forms import LoginAuthenticationForm
urlpatterns = [
	url(r'^login/$', auth_views.login,{'template_name': 'auths/login.html', 'authentication_form': LoginAuthenticationForm}, name='login')
]