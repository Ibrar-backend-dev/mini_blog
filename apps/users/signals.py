from django.db.models.signals import pre_save
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import User


@receiver(post_delete, sender=User)
def delete_profile_photo_file(sender, instance, **kwargs):
    if instance.profile_photo:
        instance.profile_photo.delete(save=False)


@receiver(pre_save, sender=User)
def delete_old_profile_photo_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        return

    old_file = old_instance.profile_photo
    new_file = instance.profile_photo

    if old_file and old_file != new_file:
        old_file.delete(save=False)