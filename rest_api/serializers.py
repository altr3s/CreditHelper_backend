from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from passlib.context import CryptContext


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print(user)
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'name', 'surname']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'name', 'surname')
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
    name = serializers.CharField()
    surname = serializers.CharField()

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(validated_data)
