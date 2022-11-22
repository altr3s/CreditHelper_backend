from django.urls import path
from .views import *

urlpatterns = [
    path('create_user/', create_user),
    path('token/', check_login),
    path('user/<int:id>/', get_user),
]
