import uuid

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.UUIDField(default=uuid.uuid4, blank=True, editable=False)
    phone = models.CharField('Teléfono', max_length=13, blank=True, null=True)

    def get_absolute_url(self):
        return '/profile/{slug}'.format(slug=self.slug)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created or not hasattr(instance, 'profile'):
        Profile.objects.create(
            user=instance
        )
    instance.profile.save()