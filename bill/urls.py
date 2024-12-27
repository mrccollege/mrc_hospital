from django.urls import path
from . import views

urlpatterns = [
    path('bill_list/', views.bill_list, name='bill_list'),
    path('patient_bill_detail/<int:id>/', views.patient_bill_detail, name='patient_bill_detail'),

    path('appointment_patient_bill_detail/<int:id>/', views.appointment_patient_bill_detail, name='appointment_patient_bill_detail'),

    path('normal_order_bill_list/', views.normal_order_bill_list, name='normal_order_bill_list'),
    path('estimate_order_bill_list/', views.estimate_order_bill_list, name='estimate_order_bill_list'),
    path('order_list/', views.order_list, name='order_list'),
    path('order_detail/<int:id>/', views.order_detail, name='order_detail'),

    path('get_patient/', views.get_patient, name='get_patient'),
    path('create_customer_bill/', views.create_customer_bill, name='create_customer_bill'),
    path('create_customer_bill_detail/<int:patient_id>/', views.create_customer_bill_detail, name='create_customer_bill_detail'),

    path('customer_generate_bill/<int:order_type>/<int:patient_id>/', views.customer_generate_bill, name='customer_generate_bill'),
]
