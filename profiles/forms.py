from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import make_password

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button, Reset
from crispy_forms.bootstrap import FormActions, PrependedText

from .models import IbkUser, Profile