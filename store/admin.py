from django.contrib import admin
from .models import Store,MedicineStore, MedicineStoreTransactionHistory

# Register your models here.
admin.site.register(Store)
admin.site.register(MedicineStore)
admin.site.register(MedicineStoreTransactionHistory)
