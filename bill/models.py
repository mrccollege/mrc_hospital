from django.db import models

from patient.models import Patient

from medicine.models import Medicine

from store.models import Store


# Create your models here.
class PatientBill(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    invoice_number = models.CharField(max_length=100, null=True)
    sgst = models.IntegerField(default=0, null=True, blank=True)
    cgst = models.IntegerField(default=0, null=True, blank=True)
    credit = models.IntegerField(default=0, null=True, blank=True)
    cash = models.IntegerField(default=0, null=True, blank=True)
    online = models.IntegerField(default=0, null=True, blank=True)
    shipping_packing = models.IntegerField(default=0, null=True, blank=True)
    discount = models.IntegerField(default=0, null=True, blank=True)
    total = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'patient_bill'


class PatientBillDetail(models.Model):
    patient_bill = models.ForeignKey(PatientBill, on_delete=models.CASCADE, null=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True)
    record_qty = models.IntegerField(default=0, null=True)
    sell_qty = models.IntegerField(default=0, null=True)
    mrp = models.IntegerField(default=0, null=True)
    discount = models.IntegerField(default=0, null=True)
    sale_rate = models.IntegerField(default=0, null=True)
    hsn = models.IntegerField(default=0, null=True)
    gst = models.IntegerField(default=0, null=True)
    amount = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'patient_bill_detail'


class SGST(models.Model):
    sgst_percent = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.sgst_percent)

    class Meta:
        db_table = 'sgst'


class CGST(models.Model):
    cgst_percent = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.cgst_percent)

    class Meta:
        db_table = 'cgst'
