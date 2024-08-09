from django.db import models

from patient.models import Patient

from medicine.models import Medicine

from store.models import Store


# Create your models here.
class PatientBill(models.Model):
    store = models.ForeignKey(Store, on_delete=models.PROTECT, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, null=True)
    invoice_number = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'patient_bill'


class PatientBillDetail(models.Model):
    patient_bill = models.ForeignKey(PatientBill, on_delete=models.PROTECT, null=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True)
    medicine_qty = models.IntegerField(null=True)
    medicine_sell_qty = models.IntegerField(null=True)
    medicine_price = models.IntegerField(null=True)
    medicine_sell_price = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'patient_bill_detail'
