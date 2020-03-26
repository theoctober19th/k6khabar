from django.urls import path
from django.contrib import admin

from .views import loginpage, logoutview

urlpatterns = [
    path('login/', loginpage, name='login'),
    path('logout/', logoutview, name='logout')
]
