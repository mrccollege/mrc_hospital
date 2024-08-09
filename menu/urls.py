from django.urls import path
from . import views

urlpatterns = [
    path('assigne_menu/', views.assigne_menu, name='assigne_menu'),
]
