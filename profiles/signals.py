from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage


from accounts.models import IbkUser, Profile

@receiver(pre_save, sender=Profile, dispatch_uid='delete_old_avatar_file_from_system')
def delete_old_avatar_file_from_system(sender, instance, **kwargs):
	try:
		image = Profile.objects.get(pk=instance.pk)
		if image.avatar.path.endswith('default_avatar.jpg'):
			pass
		else:
			default_storage.delete(image.avatar.path)
	except Profile.DoesNotExist:
		pass
