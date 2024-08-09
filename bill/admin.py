from django.contrib import admin
from .models import PatientBill, PatientBillDetail

# Register your models here.
admin.site.register(PatientBill)
admin.site.register(PatientBillDetail)
