from django.urls import path
from . import views

urlpatterns = [
    path('medicine_order/', views.medicine_order, name='medicine_order'),
]
