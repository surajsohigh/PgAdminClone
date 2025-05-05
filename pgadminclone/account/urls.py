from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('user/', UserView.as_view(), name='register'),
    path('user/<int:pk>/', UserView.as_view(), name='userDetails'),
    path('login/', LoginView.as_view(), name='login'),
    path('userprofile/', UserProfile.as_view(), name='profile'),
    path("logout/", LogoutView.as_view(), name="logout")
    
]
