from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class ProfilesConfig(AppConfig):
    name = 'profiles'

    def ready(self):
    	import profiles.signals
