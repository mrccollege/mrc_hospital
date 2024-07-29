from django.urls import path
from . import views

urlpatterns = [
    path('add_new_medicine/', views.add_new_medicine, name='add_new_medicine'),
    path('view_main_medicine/<int:id>/', views.view_main_medicine, name='view_main_medicine'),
    path('update_medicine/', views.update_medicine, name='update_medicine'),
    path('update_new_medicine/', views.update_new_medicine, name='update_new_medicine'),
    path('all_medicine/', views.all_medicine, name='all_medicine'),
]
