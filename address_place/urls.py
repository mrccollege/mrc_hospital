from django.urls import path
from . import views

urlpatterns = [
    path('get_state/', views.get_state, name='get_state'),
]
