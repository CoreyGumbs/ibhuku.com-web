from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from .views import AccountRecover
from .forms import LoginAuthenticationForm

urlpatterns = [
	url(r'^login/$', auth_views.login,{'template_name': 'auths/login.html', 'authentication_form': LoginAuthenticationForm}, name='login'),
	url(r'^logout/$', auth_views.logout,{'next_page': '/auths/login/'}, name='logout'),
	url(r'^recover/$', AccountRecover, name='recover'),
]