from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from django.db import models
from django.db.models import (
    CASCADE,
    OneToOneField,
)
from django.db.models.signals import post_save
from django.dispatch import receiver


User = get_user_model()


class Profile(models.Model):
    '''
    User profile and settings
    '''

    user = OneToOneField(User, on_delete=CASCADE)
    country = CountryField()

    def __str__(self):
        return '{} from {}'.format(
            self.user,
            self.country,
        )

    def save(self, *args, **kwargs):
        '''
        prevent unique key errors in admin
        '''

        if self.user and not self.pk:
            try:
                p = Profile.objects.get(user=self.user)
                self.pk = p.pk
            except Profile.DoesNotExist:
                pass

        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
