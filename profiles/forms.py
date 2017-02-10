from django.forms import ModelForm
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button, Reset
from crispy_forms.bootstrap import FormActions, PrependedText, FieldWithButtons

from accounts.models import IbkUser, Profile



class ProfileAvatarUploadForm(ModelForm):
	class Meta:
		model = Profile
		fields = ['avatar']
		labels = {
			'avatar': 'Upload Image'
		}

	def __init__(self, *args, **kwargs):
		super(ProfileAvatarUploadForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'avatarUploadForm'
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
				PrependedText('avatar', "<span class='glyphicon glyphicon-upload'></span>", active=True),
				FormActions(
					Submit('submit', 'Submit'),
					),
			)