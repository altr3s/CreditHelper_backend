from django.urls import path
from .views import *

urlpatterns = [
    path('register/', create_user),
    path('login/', check_login),
    path('user/<int:id>/', get_user),
]
