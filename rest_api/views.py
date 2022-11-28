from .serializers import *
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, filters
from rest_framework.decorators import api_view
import os


# api/views.py

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_api.serializers import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from braces.views import CsrfExemptMixin


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView, CsrfExemptMixin):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    authentication_classes = []


class AddCreditView(generics.CreateAPIView):
    serializer_class = CreditSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.headers.get('Authorization').split()[1]
        decoded = jwt.decode(token, options={"verify_signature": False})
        serializer = self.serializer_class(data=request.data)
        content = {
            'user_id': decoded['id'],
            'auth': request.get('auth'),
            'value': request.get('value'),
            'rate': request.get('rate'),
            'years_count': request.get('years_count'),
            'monthly_payment': request.get('monthly_payment'),
            'total_payment': request.get('total_payment'),
            'overpay': request.get('overpay'),
        }
        if serializer.is_valid():
            return Response(content, status=200)
        else:
            return Response(content, status=403)
        

class LoginAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid():
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.data, status=403)


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/',
        '/api/add_credit',
    ]
    return Response(routes)
