from django.db import models
from products.models import Products,Category
from users.models import User
# Create your models here.

class order(models.Model):
    STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class orderitem(models.Model):
    order = models.ForeignKey(order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="carts")
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

