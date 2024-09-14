from django.contrib import admin
from .models import Doctor, PatientAppointmentHead, PatientMedicine

# Register your models here.

admin.site.register(Doctor)
admin.site.register(PatientAppointmentHead)
admin.site.register(PatientMedicine)
