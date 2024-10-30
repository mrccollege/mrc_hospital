from django.contrib import admin
from .models import MedicineOrderHead, MedicineOrderDetail


# Register your models here.
# class MedicineOrderHeadAdmin(admin.ModelAdmin):
#     list_display = ('medicine', 'record_qty', 'sell_qty', 'mrp')


admin.site.register(MedicineOrderHead)
admin.site.register(MedicineOrderDetail)
