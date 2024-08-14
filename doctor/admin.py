from django.contrib import admin
from .models import Doctor, PatientAppointmentChecked, PatientAppointmentCheckedDetail

# Register your models here.

admin.site.register(Doctor)
admin.site.register(PatientAppointmentChecked)
admin.site.register(PatientAppointmentCheckedDetail)
