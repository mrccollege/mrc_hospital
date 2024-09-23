from django.urls import path
from . import views

urlpatterns = [
    path('hospital_registration/', views.hospital_registration, name='hospital_registration'),
    path('store_registration/', views.store_registration, name='store_registration'),
    path('doctor_registration/', views.doctor_registration, name='doctor_registration'),
    path('patient_registration/', views.patient_registration, name='patient_registration'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),

    path('update_user_detail/', views.update_user_detail, name='update_user_detail'),
]
