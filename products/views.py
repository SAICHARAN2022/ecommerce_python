from django.shortcuts import render
from rest_framework.views import APIView
from .models import Products,Category
from .serializers import ProductSerializer,CategorySerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class ProductList(APIView):

    def get(self,request):
        name = request.query_params.get("name", "")
        desc = request.query_params.get("desc","")
        category = request.query_params.get("category","")

        kwargs = {}
        # if not request_data:
        #     products_list = Products.objects.all()
        if name:
            kwargs["name__icontains"] = name
        if desc:
            kwargs["desc__icontains"] = desc
        if category:
            kwargs["category__name"] = kwargs
        products_list = Products.objects.filter(**kwargs)
        serializer = ProductSerializer(products_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class CategoryList(APIView):

    def get(self):
        category_list = Category.objects.all()
        serializer = CategorySerializer(category_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        


