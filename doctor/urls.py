from django.urls import path
from . import views

urlpatterns = [
    path('doctor_list/', views.doctor_list, name='doctor_list'),
    path('doctor_detail/<int:id>/', views.doctor_detail, name='doctor_detail'),
    path('patient_appointment_checked/', views.patient_appointment_checked, name='patient_appointment_checked'),
]
