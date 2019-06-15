import uuid

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    email_confirmed = models.BooleanField(default=False)
    slug = models.UUIDField(default=uuid.uuid4, blank=True, editable=False)
    phone = models.CharField('Teléfono', max_length=13, blank=True, null=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created or not hasattr(instance, 'profile'):
        Profile.objects.create(
            user=instance
        )
    instance.profile.save()

class CarProfile(models.Model):
    vehicle = models.CharField("Vehiculo", max_length=80)
    phone = models.CharField("Teléfono", max_length=20)
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '{0} - {1}'.format(self.vehicle, self.phone)