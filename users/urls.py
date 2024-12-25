from django.urls import path
from .views import *

urlpatterns = [
    path('User_Registration/',UserRegistration.as_view(),name='User_Registration'),
    path('login_view/',LoginView.as_view(),name='login_view')
]