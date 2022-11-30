from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from passlib.context import CryptContext
from django.contrib.auth import authenticate


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
        fields = '__all__'


class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = '__all__'

    def validate(self, attrs):
        return attrs

   
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


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        user = User.objects.filter(username=username).first()
        if user is None:
            raise serializers.ValidationError('Пользователь не найден')
        if not user.check_password(password):
            raise serializers.ValidationError('Неверный пароль')
        if not user.is_active:
            raise serializers.ValidationError('Пользователь деактевирован')
        return {
            'access': user.token
        }
