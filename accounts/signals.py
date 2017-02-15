from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


from accounts.models import IbkUser, Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()