from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes, name='routes'),
    path('token', views.LoginAPIView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', views.RegisterView.as_view(), name='auth_register'),
    path('add_credit', views.AddCreditView.as_view(), name='add_credit'),
    path('health', views.health, name='health'),
    path('my_credits', views.GetCreditView.as_view(), name='my_credits'),
    path('download', views.ExcelView.as_view(), name='download'),
    path('delete_credit', views.DeleteCreditFromDB.as_view(), name='delete'),
]
