from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage


from accounts.models import IbkUser, Profile

@receiver(pre_save, sender=Profile, dispatch_uid='delete_old_avatar_file_from_system')
def delete_old_avatar_file_from_system(sender, instance, **kwargs):
	default_img = 'default_avatar.jpg'
	if instance.avatar != default_img:
		image = Profile.objects.get(id=instance.id)
		default_storage.delete(image.avatar.path)
