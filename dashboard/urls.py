from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload_medicine_excel/', views.upload_medicine_excel, name='upload_medicine_excel'),
]
