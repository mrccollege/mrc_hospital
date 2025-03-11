from django.urls import path
from . import views

urlpatterns = [
    path('bill_list/', views.bill_list, name='bill_list'),
    path('patient_bill_detail/<int:id>/', views.patient_bill_detail, name='patient_bill_detail'),

    path('appointment_patient_bill_detail/<int:id>/', views.appointment_patient_bill_detail, name='appointment_patient_bill_detail'),

    path('direct_estimate_list/', views.direct_estimate_list, name='direct_estimate_list'),
    path('normal_order_bill_list/', views.normal_order_bill_list, name='normal_order_bill_list'),
    path('estimate_order_bill_list/', views.estimate_order_bill_list, name='estimate_order_bill_list'),
    path('order_list/', views.order_list, name='order_list'),
    path('order_detail/<int:id>/', views.order_detail, name='order_detail'),
    path('view_doctor_order_detail/<int:id>/', views.view_doctor_order_detail, name='view_doctor_order_detail'),
]
