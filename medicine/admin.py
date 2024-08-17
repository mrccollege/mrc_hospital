from django.contrib import admin
from .models import Medicine, MedicineCategory

# Register your models here.

admin.site.register(Medicine)
admin.site.register(MedicineCategory)
