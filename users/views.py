from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework.response import Response
import json
from .serializer import UserRegistrationSerializer
from rest_framework import status

from .models import User
from django.contrib.auth import authenticate
# Create your views here.
from ecommerce.settings import CLIENT_ID,SECRET_KEY
import requests
from rest_framework.permissions import IsAuthenticated


class UserRegistration(APIView):
    # permission_classes = [IsAuthenticated]

    def post (self,request):
        request_data = request.data

        serializer = UserRegistrationSerializer(data=request_data)
        first_name = request_data.get("first_name")
        last_name = request_data.get("last_name")
        phone_number = request_data.get("phone_number")
        password = request_data.get("password")
        if User.objects.filter(username=phone_number).exists():
            return "User Already Exist"
        user = User.objects.create(username=phone_number,first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.save()
        if user:
            return Response({"msg":"User Register Successfully"},status=status.HTTP_200_OK)
        return Response({"msg":"User Registration Failed"},status=status.HTTP_412_PRECONDITION_FAILED)
    
class LoginView(APIView):

    def post(self,request):
        request_data = request.data
        phone_number = request_data.get("phone_number")
        password = request_data.get("password")

        user_obj = User.objects.filter(username=phone_number).first()
        if not user_obj:
            return "User Does Not Exist"
        user = authenticate(username=user_obj.username,password=password)
        if user is not None:
            data = {
                "grant_type":"password",
                "username":user_obj.username,
                "password":password,
                "client_id":CLIENT_ID,
                "client_secret":SECRET_KEY
            }
            url = "http://127.0.0.1:8000/o/token/"
            response = requests.post(url=url,data=data)
            if response.status_code == 200:
                return Response(response.json(),status=status.HTTP_200_OK)
            else:
                return Response({"msg":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
                    

        


        
        

