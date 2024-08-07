from django.db import models

from doctor.models import Doctor

from patient.models import Patient


# Create your models here.
class AppointmentWard(models.Model):
    type = models.CharField(max_length=100)
    price = models.IntegerField(null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'hospital_Appointment_visit'


class PatientAppointment(models.Model):
    appoint_ward = models.ForeignKey(AppointmentWard, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    patient_diseases = models.TextField(null=True, blank=True)
    patient_bp_min = models.IntegerField(null=True, blank=True)
    patient_bp_max = models.IntegerField(null=True, blank=True)
    patient_weight = models.IntegerField(null=True, blank=True)
    fees = models.IntegerField(default=0, null=True, blank=True)
    paid = models.CharField(max_length=10, null=True, blank=True)
    remaining = models.IntegerField(default=0, null=True, blank=True)
    cash = models.IntegerField(default=0, null=True, blank=True)
    online = models.IntegerField(default=0, null=True, blank=True)
    appointment_date = models.DateField(null=True, blank=True, default=None)
    appointment_time = models.TimeField(null=True, blank=True, default=None)
    appoint_status = models.CharField(max_length=10, default='unchecked')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'patient_appointment'

    def __str__(self):
        return str(self.patient)
