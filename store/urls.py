from django.urls import path
from . import views

urlpatterns = [
    path('main_store/', views.main_store, name='main_store'),
    path('mini_store/', views.mini_store, name='mini_store'),
]
