from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    name = model.CharField(max_length=100)
    rating = model.IntegerField(default=None)
    location = model.CharField(max_length=100)
    picture = model.ImageField()
    bio = model.CharField()
    charity = model.CharField()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Item(models.Model):
    name = model.CharField(max_length=100)
    picture = model.ImageField()
    description = model.CharField(max_length=100)
    percentCharity = model.FloatField(max_length=100)
    price = model.IntegerField(default=0)
    userId = model.IntegerField()

class Charities(models.Model):
    name = model.CharField(max_length=100)
    userId = model.IntegerField()

class Cart(models.Model):
    userId = model.IntegerField()
