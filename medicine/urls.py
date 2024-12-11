from django.urls import path
from . import views

urlpatterns = [
    path('add_category/', views.add_category, name='add_category'),
    path('update_category/<int:id>/', views.update_category, name='update_category'),
    path('all_medicine_category/', views.all_medicine_category, name='all_medicine_category'),

    path('add_medicine/', views.add_medicine, name='add_medicine'),
    path('medicine_update/<int:id>/', views.medicine_update, name='medicine_update'),
    path('delete_medicine/<int:id>/', views.delete_medicine, name='delete_medicine'),
    path('all_medicine/', views.all_medicine, name='all_medicine'),

    path('add_medicine_to_store/', views.add_medicine_to_store, name='add_medicine_to_store'),
    path('view_record_medicine_detail/<int:id>/', views.view_record_medicine_detail, name='view_record_medicine_detail'),
    path('update_medicine_record/', views.update_medicine_record, name='update_medicine_record'),



    path('search_medicine/', views.search_medicine, name='search_medicine'),
    path('upload_medicine_excel/', views.upload_medicine_excel, name='upload_medicine_excel'),
]
