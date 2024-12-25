from rest_framework import serializers
from.models import Products,Category,order,Cart,CartItem,orderitem


class CartItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="product.name")
    description = serializers.CharField(source="product.description")
    category_name = serializers.CharField(source="product.category.name")
    class Meta:
        model = CartItem
        fields = [
            *[field.name for field in CartItem._meta.get_fields()],
            'name',
            'description',
            'category_name'
        ]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = order
        fields = ['id', 'user', 'total_price', 'created_at']

class OrderDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="product.name")
    description = serializers.CharField(source="product.description")
    category_name = serializers.CharField(source="product.category.name")
    price = serializers.CharField(source='product.price')

    class Meta:
        model = orderitem
        fields = ["order_id","quantity","name","description","category_name","price"]

