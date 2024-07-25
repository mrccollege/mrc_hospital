from django.urls import path
from . import views

urlpatterns = [
    path('add_medicine/', views.add_medicine, name='add_medicine'),
    path('view_medicine/<int:id>/', views.view_medicine, name='view_medicine'),
    path('update_medicine/', views.update_medicine, name='update_medicine'),
    path('all_medicine/', views.all_medicine, name='all_medicine'),
]
