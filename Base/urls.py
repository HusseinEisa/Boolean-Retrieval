from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Search, name='Search'),
    path('Result/', views.Result, name='Result'),
]
