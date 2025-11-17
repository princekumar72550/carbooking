from django.urls import path
from . import api_views

urlpatterns = [
    path('auth/register/', api_views.register, name='register'),
    path('auth/login/', api_views.login, name='login'),
]