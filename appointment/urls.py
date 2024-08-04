from django.urls import path
from . import views

urlpatterns = [
    path('add_appointment/', views.add_appointment, name='add_appointment'),
    path('search_patient/', views.search_patient, name='search_patient'),
]
