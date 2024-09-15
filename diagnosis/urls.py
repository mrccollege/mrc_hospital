from django.urls import path
from . import views

urlpatterns = [
    path('get_diagnosis_position/', views.get_diagnosis_position, name='get_diagnosis_position'),
    path('get_diagnosis_type/', views.get_diagnosis_type, name='get_diagnosis_type'),
]
