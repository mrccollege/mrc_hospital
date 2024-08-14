from django.contrib import admin
from .models import Store, MedicineStoreTransactionHistory

# Register your models here.
admin.site.register(Store)
admin.site.register(MedicineStoreTransactionHistory)
