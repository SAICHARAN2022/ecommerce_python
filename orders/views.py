from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Products,Category,Cart,CartItem,order,orderitem
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializer import *
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from django.db.models import Sum
# Create your views here.

# class CartView(APIView):

#     def get(self,request):
#         user = request.user
#         user_obj = Cart.objects.filter()

class AddToCart(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    def post(self,request):
        user = request.user
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)
        cart,created = Cart.objects.get_or_create(user=user)
        product = get_object_or_404(Products,id=product_id)
        cart_item,created = CartItem.objects.get_or_create(cart=cart,product=product)
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()
        return Response({"message":"Product added to cart"},status=status.HTTP_204_NO_CONTENT)


class CartView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    def get(self,request):
        user = request.user
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum(items.quantity * items.product.price for items in cart_items)
        serializer = CartItemSerializer(cart_items,many=True)
        data = {
            "cart_items" : serializer.data,
            "total_price" : total_price
        }
        # serializer = "ser"
        if serializer.data:
            return Response(data,status=status.HTTP_200_OK)
        return Response({"message":"Data Not Found"},status=status.HTTP_200_OK)

class DeleteFromCart(APIView):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]

    def delete(self,request):
        try:
            request_data = request.data
            user = request.user
            product = request_data.get("product_id")
            cart_item = CartItem.objects.filter(cart__user=user,product=product).delete()
            return Response({"msg":"Product removed from cart"},status=status.HTTP_200_OK)
        except CartItem.DoesNotEXist:
            return Response({"error": "Item not in cart"}, status=status.HTTP_404_NOT_FOUND)

class CreateOrder(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]
    
    def post(self,request):
        user = request.user
        cart = Cart.objects.filter(user=user).first()
        if not cart:
            return Response({"msg":"Your cart is empty"})
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum(items.product.price * items.quantity for items in cart_items)
        create_order = order.objects.create(total_price=total_price,user=user)
        # serializer = CartItemSerializer(cart_items,many=True).data
        order_items = []
        for item in cart_items:
            # Create OrderItem for each cart item
            order_item = orderitem(
                order=create_order,
                product=item.product,
                quantity=item.quantity,
            )
            order_items.append(order_item)

            # Reduce product stock
            item.product.stock -= item.quantity
            item.product.save()

        # Bulk create order items
        orderitem.objects.bulk_create(order_items)
        cart_items.delete()
        cart.delete()

        order_serializer = OrderSerializer(create_order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)

class OrderDetail(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]

    def post(self,request):
        request_data = request.data
        order_id = request_data.get('order_id')
        order_info = order.objects.get(id=order_id)
        if not order_info:
            return Response({"msg":"Order Does Not Exist"},status=status.HTTP_404_NOT_FOUND)
        order_details = orderitem.objects.filter(order=order_info.id)
        serializer = OrderDetailSerializer(order_details,many=True)
        # if serializer.is_valid():
        return Response(serializer.data,status=status.HTTP_200_OK)


class OrdersList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]

    def post(self,request):
        user_id = request.user.id
        orders_id = order.objects.filter(user=user_id).values_list('id',flat=True)
        if not orders_id:
            return Response({"msg":"Data Not Found"},status=status.HTTP_200_OK)
        orders_list = orderitem.objects.filter(order__in=orders_id)
        serializers = OrderDetailSerializer(orders_list,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

class Test(APIView):
    def get(self):
        return Response({"msg":"sucess"},status=status.HTTP_200_OK)


            




            




        

