from django.urls import path
from . import views

urlpatterns = [
    path('bill_list/', views.bill_list, name='bill_list'),
    path('patient_bill_detail/<int:id>/', views.patient_bill_detail, name='patient_bill_detail'),

    path('appointment_patient_bill_detail/<int:id>/', views.appointment_patient_bill_detail,
         name='appointment_patient_bill_detail'),

    path('order_received/<int:id>/', views.order_received, name='order_received'),
]
