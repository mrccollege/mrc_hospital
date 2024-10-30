from django.urls import path
from . import views

urlpatterns = [
    path('medicine_order/', views.medicine_order, name='medicine_order'),
    path('update_medicine_order/<int:id>/', views.update_medicine_order, name='update_medicine_order'),
    path('delete_medicine_order/<int:id>/', views.delete_medicine_order, name='delete_medicine_order'),
    path('my_medicine_ordered_list/', views.my_medicine_ordered_list, name='my_medicine_ordered_list'),
    path('search_medicine/', views.search_medicine, name='search_medicine'),

    path('create_bill/<int:order_type>/<int:id>/', views.create_bill, name='create_bill'),
    path('update_medicine_order_bill/<int:order_type>/<int:id>/', views.update_medicine_order_bill, name='update_medicine_order_bill'),
    path('estimate_medicine_order_bill/<int:order_type>/<int:id>/', views.estimate_medicine_order_bill, name='estimate_medicine_order_bill'),
]
