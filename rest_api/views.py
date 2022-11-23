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

from braces.views import CsrfExemptMixin


@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    return JsonResponse({"text":'not post'})


def health(request):
    return JsonResponse({'text':'hello world, mazafaka'})


def check_login(request, email):
    try:
        user = User.objects.filter(email=request.data.get('email'))
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(user, many=True)
        return JsonResponse(serializer.data, safe=False)



def get_user(request, id):
    try:
        user = User.objects.get(pk=id)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView, CsrfExemptMixin):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    authentication_classes = []


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/'
    ]
    return Response(routes)