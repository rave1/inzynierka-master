from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from wca.models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except Exception:
            Profile.objects.create(user=instance)


# @receiver(post_save, sender=Profile)
# def save_user_profile(sender, instance, **kwargs):
#     print("hejos")
#     instance.profile.save()
