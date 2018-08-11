from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    rating = models.IntegerField(default=0)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.CharField(max_length=2000)
    charity = models.IntegerField(default=0)
    stripe_user_id = models.CharField(max_length=200, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Item(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='item_images', blank=True)
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    charity_percent = models.IntegerField(default=0)
    charity = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    sold = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)

class Charity(models.Model):
    total_money_raised = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    mission_statement = models.CharField(max_length=1000)