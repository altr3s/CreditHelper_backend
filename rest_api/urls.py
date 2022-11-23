from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
# from .views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
urlpatterns = [
    # path('create_user/', create_user),
    # path('token/', check_login),
    # path('user/<int:id>/', get_user),
    # path('health/', health),
    path('token', views.LoginAPIView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', views.RegisterView.as_view(), name='auth_register'),
]
