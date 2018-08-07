from django.contrib import admin
from .models import Item, Charity, Cart, Profile

# Register your models here.
admin.site.register(Item)
admin.site.register(Charity)
admin.site.register(Cart)
admin.site.register(Profile)
