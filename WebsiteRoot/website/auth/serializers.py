from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist

from website.user.serializers import UserSerializer
from website.user.models import User


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user) #type:ignore

        return data


class RegisterSerializer(UserSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)
    email = serializers.EmailField(required=True, write_only=True, max_length=128)
    name = serializers.CharField(max_length=128, min_length=8, write_only=True)
    surname = serializers.CharField(max_length=128, min_length=8, write_only=True)
    username = serializers.CharField(max_length=128, min_length=8, write_only=True)
    

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        try:
            user = User.objects.get(email=validated_data['email', 'username'])
        except ObjectDoesNotExist:
            user = User.objects.create_user(**validated_data)
        return user
