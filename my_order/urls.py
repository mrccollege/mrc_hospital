from django.urls import path
from . import views

urlpatterns = [
    path('medicine_order/', views.medicine_order, name='medicine_order'),
    path('update_medicine_order/<int:id>/', views.update_medicine_order, name='update_medicine_order'),
    path('delete_medicine_order/<int:id>/', views.delete_medicine_order, name='delete_medicine_order'),
    path('my_medicine_ordered_list/', views.my_medicine_ordered_list, name='my_medicine_ordered_list'),
    path('search_medicine/', views.search_medicine, name='search_medicine'),
]
