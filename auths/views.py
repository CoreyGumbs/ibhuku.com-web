from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic.edit import FormView


from accounts.models import IbkUser, Profile
from accounts.accountslib import profile_validation_key, check_profile_validation_key
from auths.authlib import password_reset_link
from .forms import LoginAuthenticationForm, AccountRecoveryForm

# Create your views here.
@csrf_protect
def AccountRecover(request):
	if request.method == 'POST':
		form = AccountRecoveryForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			try:
				user= IbkUser.objects.get(email__iexact=email)
				token = default_token_generator.make_token(user)
				if user:
					profile = Profile.objects.get(user_id=user.id)
					profile.verified = False
					profile.verify_key = token
					profile.save()
					password_reset_link(user, email, token, request=request)
					return HttpResponse('thank you. Email sent.')
			except IbkUser.DoesNotExist:
				pass
	else:
		form = AccountRecoveryForm()
	context = {
		'form': form,
	}
	return render(request, 'auths/recover.html', context)

def AccountResetLinkConfirm(request, uidb64=None, token=None, token_generator=default_token_generator):
	return HttpResponse("Comfirmed Account")