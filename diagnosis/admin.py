from django.contrib import admin
from .models import DiagnosisDiseaseName, DiagnosisPosition, DiagnosisType

# Register your models here.
admin.site.register(DiagnosisDiseaseName)
admin.site.register(DiagnosisPosition)
admin.site.register(DiagnosisType)
