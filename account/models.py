from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils.translation import gettext_lazy as _
from django.db import models
# Create your models here.
class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')
        
        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

class UserBase(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField( max_length=50, unique=True)
    first_name = models.CharField( max_length=50, blank=True)
    phone_number = models.CharField( max_length=15, blank=True)
    postcode = models.CharField(max_length=10, blank=True)
    address = models.CharField(max_length=50, blank= True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.user_name

class ShippingAddress(models.Model):
    user = models.ForeignKey(UserBase, on_delete=models.CASCADE)
    first_name = models.CharField( max_length=32)
    phone_number = models.CharField( max_length=16)
    postcode = models.CharField(max_length=8)
    address = models.CharField(max_length=64)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=16)
    country = models.CharField(max_length=16)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    default = models.BooleanField(_("Default"), default=False)

    class Meta:
        verbose_name_plural = 'shipping_address'
        ordering = ('-created',)