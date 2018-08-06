from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    name = models .CharField(max_length=100)
    rating = models.IntegerField(default=None)
    location = models.CharField(max_length=100)
    picture = models.CharField(max_length=100)
    bio = models.CharField(max_length=2000)
    charity = models.CharField(max_length=100)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Item(models.Model):
    name = models.CharField(max_length=100)
    picture = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    percentCharity = models.FloatField(max_length=100)
    price = models.IntegerField(default=0)
    userId = models.IntegerField()

class Charity(models.Model):
    name = models.CharField(max_length=100)
    userId = models.IntegerField()

class Cart(models.Model):
    userId = models.IntegerField()
