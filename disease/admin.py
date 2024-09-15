from django.contrib import admin
from .models import Since, Severity, Bleeding

# Register your models here.
admin.site.register(Since)
admin.site.register(Severity)
admin.site.register(Bleeding)
