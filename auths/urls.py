from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from .views import AccountRecover, AccountResetLinkConfirm, PasswordResetDone
from .forms import LoginAuthenticationForm

urlpatterns = [
	url(r'^login/$', auth_views.login,{'template_name': 'auths/login.html', 'authentication_form': LoginAuthenticationForm}, name='login'),
	url(r'^logout/$', auth_views.logout,{'next_page': '/auths/login/'}, name='logout'),
	url(r'^recover/$', AccountRecover, name='recover'),
	url(r'^recover/done/$', PasswordResetDone.as_view(), name='recover-done'),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', AccountResetLinkConfirm, name='recover-password'),

]