from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.files.storage import default_storage
from django.contrib import messages

from profiles.forms import ProfileAvatarUploadForm
from accounts.models import IbkUser, Profile

# Create your views here.
@login_required
def ProfileDashboardView(request, name=None):
	usr_name = IbkUser.objects.get(name=name)
	usr_profile = Profile.objects.get(user_id=usr_name.id)
	avatar_form = ProfileAvatarUploadForm(request.FILES, request.POST)
	avatar_form.helper.form_action = reverse('profile:avatar-upload', kwargs={'name': name})

	context = {
		'user': usr_name,
		'profile': usr_profile,
		'avatar_form': avatar_form,
	}
	return render(request, 'profiles/profile_dashboard.html', context)

@login_required
def ProfileAvatarUploadView(request, name):
	usr_profile = Profile.objects.select_related('user').get(user_id=request.user.id)
	if request.method == 'POST':
		form = ProfileAvatarUploadForm(request.FILES, request.POST, instance=usr_profile)
		if form.is_valid():
			profile = form.save(commit=False)
			try:
				profile.avatar = request.FILES['avatar']
				profile.save()
				messages.success(request, 'Your avatar was updated successfully!', extra_tags='message-success')
				return HttpResponseRedirect(reverse('profile:dashboard', kwargs={'name': name}))
			except KeyError:
				messages.error(request, 'No avatar was uploaded. Please try again.', extra_tags='message-error')
				return HttpResponseRedirect(reverse('profile:dashboard', kwargs={'name': name}))
	else:
		return HttpResponseRedirect(reverse('profile:dashboard', kwargs={'name': name}))

