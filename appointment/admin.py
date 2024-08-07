from django.contrib import admin
from .models import AppointmentWard, PatientAppointment

# Register your models here.
admin.site.register(AppointmentWard)
admin.site.register(PatientAppointment)
