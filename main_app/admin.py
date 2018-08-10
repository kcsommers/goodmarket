from django.contrib import admin
from .models import Item, Cart, Profile, Charity

# Register your models here.
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(Profile)
admin.site.register(Charity)
