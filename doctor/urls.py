from django.urls import path
from . import views

urlpatterns = [
    path('list_doctor/', views.list_doctor, name='list_doctor'),
]
