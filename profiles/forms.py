from django.forms import ModelForm

from accounts.models import IbkUser, Profile



class ProfileAvatarUploadForm(ModelForm):
	class Meta:
		model = Profile
		fields=('avatar', )