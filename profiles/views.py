from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from accounts.models import IbkUser, Profile

# Create your views here.
@login_required
def ProfileDashboardView(request, name=None):
	usr_name = IbkUser.objects.get(name=name)
	context = {
		'user': usr_name,
	}
	return render(request, 'profiles/profile_dashboard.html', context)

@login_required
def ProfileAvatarUploadView(request, name=None):
	usr_name = IbkUser.objects.get(name=name)
	context = {
		'my_name': usr_name,
	}
	return render(request, 'profiles/profile_avatar_upload.html', context)