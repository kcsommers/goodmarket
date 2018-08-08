from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    id = models.IntegerField(primary_key=True, default=0)
    rating = models.IntegerField(default=None)
    location = models.CharField(max_length=100)
    picture = models.CharField(max_length=100)
    bio = models.CharField(max_length=2000)
    charity = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    charity_percent = models.FloatField(max_length=100)
    charity = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    sold = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Charity(models.Model):
    name = models.CharField(max_length=100)
    userId = models.IntegerField()
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
