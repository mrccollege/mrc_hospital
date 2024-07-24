from django.urls import path
from . import views

urlpatterns = [
    path('add_medicine/', views.add_medicine, name='add_medicine'),
]
