from django.contrib import admin
from .models import Store, MainStoreMedicine, MainStoreMedicineTransaction

# Register your models here.
admin.site.register(Store)
admin.site.register(MainStoreMedicine)
admin.site.register(MainStoreMedicineTransaction)
