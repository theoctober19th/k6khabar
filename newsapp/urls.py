from django.urls import path
from django.contrib import admin

from .views import index, detail, categorynews

urlpatterns = [
    path('', index, name='index'),
    path('detail/<int:id>/', detail, name='detail'),
    path('topic/<int:id>/', categorynews, name='topic')
]
