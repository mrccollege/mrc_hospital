from django.contrib import admin
from .models import PatientBill, PatientBillDetail, SGST, CGST

# Register your models here.
admin.site.register(PatientBill)
admin.site.register(PatientBillDetail)
admin.site.register(SGST)
admin.site.register(CGST)
