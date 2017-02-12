from django.forms import ModelForm
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button, Reset, Field
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
		self.helper.fsorm_method = 'post'
		self.helper.form_show_labels = False
		self.helper.layout = Layout(
				Field('avatar'),
				FormActions(
					Submit('submit', 'Submit'),
					Button('cancel', 'Cancel', css_class="btn-danger",
                        data_dismiss="modal", aria_hidden="true")
					),
			)