from typing_extensions import Required
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from numpy import require
from .choices import countrys,GENDER_CHOICES  

# Create your models here.

# Account model
class MyAccountManager(BaseUserManager):
    def create_user(self,firstname,lastname,username,email,password=None):
        if not email:
            raise ValueError('User must have an email ')
        if not username:
            raise ValueError('user must have an username')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            firstname=firstname,
            lastname=lastname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
        

    def create_superuser(self,firstname,lastname,username,email,password):
      
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            firstname=firstname,
            lastname=lastname,            
        )

        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user
   
class Account(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username','firstname','lastname']
    objects=MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True


class Customer(models.Model):
    
    id = models.AutoField(primary_key=True)
    choose_user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='customer',on_delete=models.CASCADE)
    #owner = models.ForeignKey('auth.User', related_name='customer_name', on_delete=models.CASCADE)
    #user=models.ForeignKey(settings.AUTH_USER_MODEL)
    #choose_user=models.ForeignKey(Account,on_delete=models.CASCADE) 
    customer_name=models.CharField(max_length=30)
    age=models.IntegerField()
    country=models.CharField(max_length=150,choices=countrys)
    gender=models.CharField(max_length=30,choices=GENDER_CHOICES)

    def __str__(self):
        return self.customer_name

    #REQUIRED_FIELDS = ['customer_name','age','country','gender','choose_user']
