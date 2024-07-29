from django.contrib import admin
from .models import Store, MainStoreMedicine, MainToMiniStoreMedicine, MainStoreMedicineTransaction

# Register your models here.
admin.site.register(Store)
admin.site.register(MainStoreMedicine)
admin.site.register(MainToMiniStoreMedicine)
admin.site.register(MainStoreMedicineTransaction)
