from django.urls import path
from . import views

urlpatterns = [
    path('hospital_registration/', views.hospital_registration, name='hospital_registration'),
    path('store_registration/', views.store_registration, name='store_registration'),
]
