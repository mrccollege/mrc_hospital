from django.urls import path
from . import views

urlpatterns = [
    path('patient_list/', views.patient_list, name='patient_list'),
    path('patient_detail/<int:id>/', views.patient_detail, name='patient_detail'),
]
