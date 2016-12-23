from django.conf.urls import include, url
from django.views.generic.edit import CreateView

from accounts.views import AccountsIndex, AccountSignUp, AccountActivation, ResetLinkActivation

urlpatterns = [
    url(r'^$', AccountsIndex.as_view(), name='index'),
    url(r'^register/$', AccountSignUp.as_view(), name='sign-up'),
    url(r'^activation/(?P<verify_key>[\w@.:]+[\w])/$', AccountActivation, name='activation'),
    url(r'^reset/(?P<user_id>\d+)$', ResetLinkActivation.as_view(), name='link_reset'),
 ]