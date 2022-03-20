from django.conf.urls import url
from django.urls import path, include
from .api import *

urlpatterns = [
      path('api/UserRegister',UserRegisterApi.as_view()),
      path('api/UserView',UserViewApi.as_view()),
      path('api/UserLogin',UserLoginApi.as_view()),
      path('api/CustomerRegister',CustomerRegisterApi.as_view()),
      path('api/ListCustomerDetails/<int:pk>',ListCustomerApi.as_view()),
      path('api/ListCustomerDetails',ListCustomerApi.as_view()),
      path('api/TargetCustomer',TargetCustomerApi.as_view()),
      path('api/UserLogout',LogoutViewApi.as_view()),

]

      