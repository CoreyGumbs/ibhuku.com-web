from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from django.views.generic.edit import CreateView

from accounts.views import CreateUserAccountView, LinkActivationView, ResetActivationLink, ActivationLinkSentMessage, AccountErrorMessage

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('accounts:register')), name='index'),
    url(r'^register/$', CreateUserAccountView.as_view()	, name='register'),
    url(r'^activate/$', AccountErrorMessage, name='account-error'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', LinkActivationView, name='activate'),
    url(r'^reset/$', ResetActivationLink, name='account-reset'),
    url(r'^sent/$', ActivationLinkSentMessage.as_view(), name='activation-sent'),
    url(r'^error/$', AccountErrorMessage.as_view(), name='account-error'),
 ]