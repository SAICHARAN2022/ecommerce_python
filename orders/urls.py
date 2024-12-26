from django.urls import path
from .views import *

urlpatterns = [
    path('add_to_cart/',AddToCart.as_view(),name='add_to_cart'),
    path('cart_view/',CartView.as_view(),name='cart_view'),
    path('delete_from_cart/',DeleteFromCart.as_view(),name='delete_from_cart'),
    path('Create_Order/',CreateOrder.as_view(),name='Create_Order'),
    path('order_detail/',OrderDetail.as_view(),name='order_detail'),
    path('list_of_orders/',OrdersList.as_view(),name='list_of_orders'),
    path('test/',Test.as_view(),name='test')


]