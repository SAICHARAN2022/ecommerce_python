from rest_framework import serializers
from .models import  User

class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=True)
    phone_number = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)

    def validate_first_name(self,value):
        if not value:
            raise serializers.ValidationError("Please Provide First Name")
        return value

    def validate_last_name(self,value):
        if not value:
            raise serializers.ValidationError("Please Provide Last Name")
        return value
    def validate_phone_number(self,value):
        x = value
        if not len(value)==10:
            raise serializers.ValidationError("Enter Valid Phone Number")
        return value

    def validate_password(self,value):
        if not value:
            raise serializers.ValidationError("Please Set Your Password")
        return value

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'password']
