from django.urls import path
from . import views

urlpatterns = [
    path('bill_list/', views.bill_list, name='bill_list'),
]
