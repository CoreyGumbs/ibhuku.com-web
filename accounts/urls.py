from django.conf.urls import include, url
from django.views.generic.edit import CreateView

from accounts.views import AccountsIndex, AccountSignUp

urlpatterns = [
    url(r'^$', AccountsIndex.as_view(), name='index'),
    url(r'register/$', AccountSignUp.as_view(), name='sign-up'),
 ]