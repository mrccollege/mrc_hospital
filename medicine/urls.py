from django.urls import path
from . import views

urlpatterns = [
    path('add_medicine/', views.add_medicine, name='add_medicine'),
    path('all_medicine/', views.all_medicine, name='all_medicine'),
]
