from django.urls import path
from . import views

urlpatterns = [
    path('assign_menu/', views.assign_menu, name='assign_menu'),
    path('get_user_data/', views.get_user_data, name='get_user_data'),
    path('get_menu_data/', views.get_menu_data, name='get_menu_data'),
    path('save_selected_menus/', views.save_selected_menus, name='save_selected_menus'),
]
