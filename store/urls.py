from django.urls import path
from . import views

urlpatterns = [
    path('main_store/', views.main_store, name='main_store'),
    path('transfer_new_main_store_medicine_detail/<int:id>/', views.transfer_new_main_store_medicine_detail, name='transfer_new_main_store_medicine_detail'),
    path('transfer_mini_store_medicine_detail/<int:record_id>/', views.transfer_mini_store_medicine_detail, name='transfer_mini_store_medicine_detail'),
    path('transfer_new_medicine_from_main/<int:id>/', views.transfer_new_medicine_from_main, name='transfer_new_medicine_from_main'),
    path('transfer_medicine_from_mini/', views.transfer_medicine_from_mini, name='transfer_medicine_from_mini'),
    path('medicine_add_transaction_history/', views.medicine_add_transaction_history, name='add_transaction_history'),
    path('mini_store/', views.mini_store, name='mini_store'),
    path('view_mini_store_medicine/<int:store_id>/', views.view_mini_store_medicine, name='view_mini_store_medicine'),
]
