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
        fields = ['id', 'username', 'email', 'pwd', 'name', 'surname']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'pwd', 'email', 'name', 'surname')
    username = serializers.CharField()
    email = serializers.CharField()
    pwd = serializers.CharField()
    name = serializers.CharField()
    surname = serializers.CharField()


    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        print(validated_data)
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        user.pwd = pwd_context.hash(validated_data['pwd'])
        user.save()
        return user
