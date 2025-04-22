from django.urls import path
from . import views

urlpatterns = [
    path('patient_procedure/', views.patient_procedure, name='patient_procedure'),
    path('create_procedure/<int:patient_id>/', views.create_procedure, name='create_procedure'),
    path('update_procedure/<int:id>/', views.update_procedure, name='update_procedure'),
    path('view_procedure_invoice/<int:id>/', views.view_procedure_invoice, name='view_procedure_invoice'),
    path('procedure_list/', views.procedure_list, name='procedure_list'),
    path('get_procedure/', views.get_procedure, name='get_procedure'),
]
