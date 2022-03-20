from rest_framework import serializers
from django.db import models
from django.contrib.auth.models import User
from .models import Account,Customer
from django.core import serializers as core_serializers
from django.http import HttpResponse
from rest_framework.authtoken.models import Token

# Register serializer
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        extra_kwargs = {'email' :{'required': True}} 
        extra_kwargs = {'password' :{'required': True}} 
        extra_kwargs = {'firstname' :{'required': True}} 
        extra_kwargs = {'lastname' :{'required': True}} 
        extra_kwargs = {'username' :{'required': True}} 
        extra_kwargs = {'is_active' :{'required': True}} 

    def create(self, validated_data):
        user = super(UserRegisterSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

# User serializer
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        fields = ('email','username')
      

# Customer serializer
class RegisterCustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {'Customer Name' :{'required': True}} 
        extra_kwargs = {'Age' :{'required': True}} 
        extra_kwargs = {'Country' :{'required': True}} 
        extra_kwargs = {'Gender' :{'required': True}} 
        extra_kwargs = {'Choose User' :{'required': True}} 

    def create(self, validated_data):
        user = super(RegisterCustomerSerializer, self).create(validated_data)
        user.save()
        return user

# list of customer serializer
class GetCustomerDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = ('id','customer_name','age','country','gender')  
        
#user Login serializers
class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'email' :{'required': True}} 
        extra_kwargs = {'password' :{'required': True}} 
        

#userview serializser
class UserViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email','username')

#User Logout view serializers
class LogoutViewSerializer(serializers.ModelSerializer):

     class Meta:
         model = User
         fields = ( 'email', 'password')      

