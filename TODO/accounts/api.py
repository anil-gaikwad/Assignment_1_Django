import email
from urllib import request
from numpy import choose
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.response import Response

from .serializers import *
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
User = get_user_model()


# Register API
class UserRegisterApi(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

# Register Customer API
class CustomerRegisterApi(generics.GenericAPIView):
    serializer_class = RegisterCustomerSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "Customer Created Successfully."
        })


# List of Customer API
class ListCustomerApi(APIView):
    serializer_class = GetCustomerDataSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    # def get(self, request,*args,  **kwargs):
    #     serializer = GetCustomerDataSerializer(Customer.objects.filter(choose_user='1'),many=True)
        
    #     return Response({
    #         "Customer": serializer.data,
    #     })
    def get(self, request,*args,  **kwargs):
       
        serializer = GetCustomerDataSerializer(Customer.objects.filter(choose_user=request.user.pk),many=True)
        return Response({
            "customer" : serializer.data
        })
        
    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404


    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response({
            "Messages" :"Customer Deleted Successfully"
        })

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = GetCustomerDataSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({
            "Messages" :"Customer Update Successfully"
        },serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

# List of Target Customer API    
class TargetCustomerApi(APIView):
    serializers_class=GetCustomerDataSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self,request,*args,  **kwargs):
        serializer_male=Customer.objects.filter(age__gte=18, age__lte=50, gender='Male', country__in=["US", "IN", "EN", "AU", "FR"],choose_user=request.user.pk)
        serializer_female=Customer.objects.filter(age__gte=15, age__lte=45, gender='Female',country__in=["US", "IN", "EN", "AU", "FR"],choose_user=request.user.pk)
        datasetmale = GetCustomerDataSerializer(serializer_male,many=True)

        datasetfemale=GetCustomerDataSerializer(serializer_female,many=True)
        return Response(
            {
                "Target-Customer-Male":datasetmale.data,
                "Target-Customer-Female":datasetfemale.data,
            },
            status=status.HTTP_200_OK       
        )
#User Login API
class UserLoginApi(APIView):
    serializers_class = UserLoginSerializer
    
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response



# User View API
class UserViewApi(APIView):
    serializers_class = UserSerializer
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

# User Logout view
class LogoutViewApi(APIView):
    serializers_class = LogoutViewSerializer
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': ' Logout successfully'
        }
        return response

