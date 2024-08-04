from django.urls import path
from . import views

urlpatterns = [
    path('doctor_list/', views.doctor_list, name='doctor_list'),
    path('doctor_detail/<int:id>/', views.doctor_detail, name='doctor_detail'),
]
