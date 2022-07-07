
from django.conf import settings
from django.db import models

from account.models import ShippingAddress
from store.models import Product

# Create your models here.
class Order(models.Model):
    order_key = models.CharField(max_length=128)
    payment_id = models.CharField(max_length=128)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipp_addr = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)
    amount = models.IntegerField()
    created = models.DateTimeField( auto_now_add=True)
    updated = models.DateTimeField( auto_now=True)
    billing_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = "orders"
        ordering = ('-created',)
    
    def __str__(self):
        return self.created
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.id

