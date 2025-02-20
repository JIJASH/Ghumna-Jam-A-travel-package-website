from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('login',login_view, name='login'),
    path('register',register_view , name='register'),
    path('logout', include('django.contrib.auth.urls')),
    # path('userdetails',user_details),
    # path('updatedetails',update_customer_details),
]
