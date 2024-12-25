from django.db import models
from users.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=125)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

class Products(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)