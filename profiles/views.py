from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from profiles.forms import ProfileAvatarUploadForm
from accounts.models import IbkUser, Profile

# Create your views here.
@login_required
def ProfileDashboardView(request, name=None):
	usr_name = IbkUser.objects.get(name=name)
	usr_profile = Profile.objects.select_related('user').get(user_id=usr_name.id)
	avatar_form = ProfileAvatarUploadForm(request.FILES, request.POST or None)
	context = {
		'user': usr_name,
		'profile': usr_profile,
		'avatar_form': avatar_form,
	}
	return render(request, 'profiles/profile_dashboard.html', context)

@login_required
def ProfileAvatarUploadView(request, name=None, pk=None):
	usr_profile = Profile.objects.select_related('user').get(user_id=pk)
	form = ProfileAvatarUploadForm(request.FILES, request.POST or None)
	form.helper.form_action = reverse('profile:avatar-upload', kwargs={'name': name, 'pk': pk})
	context = {
		'profile': usr_profile,
		'form': form,
	}
	return render(request, 'profiles/profile_avatar_upload.html', context)
