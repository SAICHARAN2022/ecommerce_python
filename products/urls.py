from django.urls import path
from .views import *

urlpatterns = [
    path('product_list/',ProductList.as_view(),name='add_to_cart'),
    path('cart_view/',CategoryList.as_view(),name='cart_view')
]