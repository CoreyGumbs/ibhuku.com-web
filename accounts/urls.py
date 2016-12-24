from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from django.views.generic.edit import CreateView

from accounts.views import AccountSignUp, AccountActivation, ResetLinkActivation, VerifiedAccountMessage, ResetLinkErrorMessage, ActivationLinkSentMessage

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('accounts:register')), name='index'),
    url(r'^register/$', AccountSignUp.as_view(), name='register'),
    url(r'^activation/(?P<verify_key>[\w@.:]+[\w])/$', AccountActivation, name='activation'),
    url(r'^reset/(?P<user_id>\d+)$', ResetLinkActivation.as_view(), name='link_reset'),
    url(r'^sent/$', ActivationLinkSentMessage.as_view(), name='activation-sent'),
    url(r'^verified/$', VerifiedAccountMessage.as_view(), name='verified'),
    url(r'^reset-error/$', ResetLinkErrorMessage.as_view(), name='reset-error'),
 ]