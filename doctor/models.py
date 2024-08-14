from django.db import models

from account.models import User

from patient.models import Patient

from medicine.models import Medicine


# Create your models here.
class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    specialist = models.CharField(max_length=100, null=True)
    degree = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        db_table = 'doctor'


class PatientAppointmentChecked(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, null=True)
    doctor_diseases = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.patient.user.username)


class PatientAppointmentCheckedDetail(models.Model):
    head_id = models.ForeignKey(PatientAppointmentChecked, on_delete=models.PROTECT, null=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT, null=True)
    qty = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.medicine.medicine_name)
