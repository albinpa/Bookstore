from django.contrib import admin
from .models import ShippingAddress, UserBase

admin.site.register(UserBase)
admin.site.register(ShippingAddress)
# Register your models here.
