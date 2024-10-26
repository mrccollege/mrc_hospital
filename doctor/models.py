from django.db import models

from account.models import User

from patient.models import Patient

from medicine.models import Medicine

from disease.models import Since, Severity, Bleeding

from diagnosis.models import DiagnosisDiseaseName, DiagnosisPosition, DiagnosisType

from previous_treatment.models import PreviousTreatment


# Create your models here.
class Doctor(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    specialist = models.CharField(max_length=100, null=True)
    degree = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        db_table = 'doctor'


class PatientAppointmentHead(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    p_r = models.CharField(max_length=100, null=True, blank=True)
    procto = models.CharField(max_length=100, null=True, blank=True)
    probing = models.CharField(max_length=100, null=True, blank=True)
    o_e = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.patient.user.username)

    class Meta:
        db_table = 'patient_appointment_head'


class ChiefComplaints(models.Model):
    head = models.ForeignKey(PatientAppointmentHead, on_delete=models.CASCADE, null=True)
    complaints = models.TextField(null=True, blank=True)
    since = models.ForeignKey(Since, on_delete=models.CASCADE, null=True)
    severity = models.ForeignKey(Severity, on_delete=models.CASCADE, null=True)
    bleeding = models.ForeignKey(Bleeding, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.head.patient)

    class Meta:
        db_table = 'chief_complaints'


class OtherAssociatesComplaints(models.Model):
    head = models.ForeignKey(PatientAppointmentHead, on_delete=models.CASCADE, null=True)
    complaints = models.TextField(null=True, blank=True)
    since = models.ForeignKey(Since, on_delete=models.CASCADE, null=True)
    severity = models.ForeignKey(Severity, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.head.patient)

    class Meta:
        db_table = 'other_associates_complaints'


class PatientMedicine(models.Model):
    head = models.ForeignKey(PatientAppointmentHead, on_delete=models.CASCADE, null=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True)
    qty = models.IntegerField(default=0, null=True)
    dose = models.CharField(max_length=100, null=True, blank=True)
    interval = models.CharField(max_length=100, null=True, blank=True)
    dose_with = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.medicine.medicine_name)

    class Meta:
        db_table = 'patient_medicine'


class PatientAppointmentImage(models.Model):
    head = models.ForeignKey(PatientAppointmentHead, on_delete=models.CASCADE, null=True)
    image = models.FileField(upload_to='patient_appointment_image', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.head.patient)

    class Meta:
        db_table = 'patient_appointment_image'


class PatientAppointmentDiagnosis(models.Model):
    head = models.ForeignKey(PatientAppointmentHead, on_delete=models.CASCADE, null=True)
    disease = models.ForeignKey(DiagnosisDiseaseName, on_delete=models.CASCADE, null=True)
    position = models.ForeignKey(DiagnosisPosition, on_delete=models.CASCADE, null=True)
    type = models.ForeignKey(DiagnosisType, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.head.patient)

    class Meta:
        db_table = 'patient_appointment_diagnosis'


class PreviousTreatmentAppointmentDetails(models.Model):
    head = models.ForeignKey(PatientAppointmentHead, on_delete=models.CASCADE, null=True)
    history = models.CharField(max_length=100, null=True, blank=True)
    remark = models.ForeignKey(PreviousTreatment, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.head.patient)

    class Meta:
        db_table = 'previous_treatment_appointment_details'
