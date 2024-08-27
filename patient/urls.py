from django.urls import path
from . import views

urlpatterns = [
    path('patient_list/', views.patient_list, name='patient_list'),
    path('patient_detail/<int:id>/', views.patient_detail, name='patient_detail'),
    path('search_patient/', views.search_patient, name='search_patient'),
    path('add_other_reference/', views.add_other_reference, name='add_other_reference'),
]
