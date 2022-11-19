from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include(('website.routers', 'website'), namespace='website-api')),
]