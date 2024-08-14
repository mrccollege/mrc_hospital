from django.urls import path
from . import views

urlpatterns = [
    path('add_new_medicine/', views.add_new_medicine, name='add_new_medicine'),
    path('add_medicine_to_store/', views.add_medicine_to_store, name='add_medicine_to_store'),
    path('medicine_update/<int:id>/', views.medicine_update, name='medicine_update'),
    path('view_main_medicine/<int:id>/', views.view_main_medicine, name='view_main_medicine'),
    path('update_new_medicine/', views.update_new_medicine, name='update_new_medicine'),
    path('all_medicine/', views.all_medicine, name='all_medicine'),


    path('search_medicine/', views.search_medicine, name='search_medicine'),
    path('upload_medicine_excel/', views.upload_medicine_excel, name='upload_medicine_excel'),
]
