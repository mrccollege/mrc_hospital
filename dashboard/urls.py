from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('get_menu_data/', views.get_menu_data, name='get_menu_data'),
]
