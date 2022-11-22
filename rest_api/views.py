from .serializers import *
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, filters
import os


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def check_login(request, email):
    try:
        user = User.objects.filter(email=request.data.get('email'))
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(user, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def get_user(request, id):
    try:
        user = User.objects.get(pk=id)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)
