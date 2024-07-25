from django.urls import path
from . import views

urlpatterns = [
    path('main_store/', views.main_store, name='main_store'),
    path('transfer_medicine_detail/<int:id>/', views.transfer_medicine_detail, name='transfer_medicine_detail'),
    path('transfer_medicine_from_main/', views.transfer_medicine_from_main, name='transfer_medicine_from_main'),
    path('medicine_add_transaction_history/', views.medicine_add_transaction_history, name='add_transaction_history'),
    path('mini_store/', views.mini_store, name='mini_store'),
    path('view_mini_store_medicine/<int:id>/', views.view_mini_store_medicine, name='view_mini_store_medicine'),
]
