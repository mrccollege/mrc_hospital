from django.contrib import admin
from .models import Medicine, MedicineCategory

# Register your models here.
class MedicineCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')

admin.site.register(Medicine)
admin.site.register(MedicineCategory, MedicineCategoryAdmin)
