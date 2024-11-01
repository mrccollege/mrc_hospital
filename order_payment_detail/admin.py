from django.contrib import admin
from .models import PaymentDetail


# Register your models here.
class PaymentDetailAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'ifc_number', 'upi_id_number']


admin.site.register(PaymentDetail, PaymentDetailAdmin)
