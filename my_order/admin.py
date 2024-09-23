from django.contrib import admin
from .models import MedicineOrderHead, MedicineOrderDetail

# Register your models here.

admin.site.register(MedicineOrderHead)
admin.site.register(MedicineOrderDetail)
