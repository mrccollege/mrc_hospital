from django.urls import path
from . import views

urlpatterns = [
    path('add_appointment/', views.add_appointment, name='add_appointment'),
    path('update_appointment/<int:id>/', views.update_appointment, name='update_appointment'),
    path('all_appointment/', views.all_appointment, name='all_appointment'),
    path('search_patient/', views.search_patient, name='search_patient'),

    path('patient_appointment_detail/<int:id>/', views.patient_appointment_detail, name='patient_appointment_detail'),
]
