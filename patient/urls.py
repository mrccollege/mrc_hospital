from django.urls import path
from . import views

urlpatterns = [
    path('patient_list/', views.patient_list, name='patient_list'),
    path('patient_detail/<int:id>/', views.patient_detail, name='patient_detail'),
    path('search_patient/', views.search_patient, name='search_patient'),
    path('add_other_reference/', views.add_other_reference, name='add_other_reference'),


    path('get_patient/', views.get_patient, name='get_patient'),
    path('create_patient_bill/', views.create_patient_bill, name='create_patient_bill'),
    path('create_patient_bill_detail/<int:patient_id>/', views.create_patient_bill_detail, name='create_patient_bill_detail'),

    path('patient_generate_bill/<int:order_type>/<int:patient_id>/', views.patient_generate_bill, name='patient_generate_bill'),


    path('create_bill/<int:order_type>/<int:patient_id>/', views.create_bill, name='create_bill'),
    path('update_medicine_order_bill/<int:order_type>/<int:id>/', views.update_medicine_order_bill, name='update_medicine_order_bill'),

    path('unregistered_create_bill/<int:order_type>/<int:id>/', views.unregistered_create_bill, name='unregistered_create_bill'),

    path('estimate_medicine_order_bill/<int:order_type>/<int:id>/', views.estimate_medicine_order_bill, name='estimate_medicine_order_bill'),
    path('update_estimate_medicine_order_bill/<int:order_type>/<int:id>/', views.update_estimate_medicine_order_bill, name='update_estimate_medicine_order_bill'),

    path('normal_order_bill_list/', views.normal_order_bill_list, name='normal_order_bill_list'),
    path('estimate_order_bill_list/', views.estimate_order_bill_list, name='estimate_order_bill_list'),

    path('view_normal_invoice/<int:id>/', views.view_normal_invoice, name='view_normal_invoice'),
    path('final_bill_invoice/<int:id>/', views.final_bill_invoice, name='final_bill_invoice'),
    path('view_estimate_invoice/<int:id>/', views.view_estimate_invoice, name='view_estimate_invoice'),


    path('add_extra_amount/<int:id>/', views.add_extra_amount, name='add_extra_amount'),
    path('estimate_add_extra_amount/<int:id>/', views.estimate_add_extra_amount, name='estimate_add_extra_amount'),
    path('export_today_patient_bills_excel/', views.export_today_patient_bills_excel, name='export_today_patient_bills_excel'),
]
