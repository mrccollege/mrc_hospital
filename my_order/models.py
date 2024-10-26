from django.db import models

from doctor.models import Doctor

from medicine.models import Medicine

from store.models import Store


# Create your models here.
class MedicineOrderHead(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    subtotal = models.FloatField(default=0, null=True)
    discount = models.IntegerField(default=0, null=True)
    shipping = models.FloatField(default=0, null=True)
    pay_amount = models.FloatField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.doctor)

    class Meta:
        db_table = 'medicine_order_head'


class MedicineOrderDetail(models.Model):
    head = models.ForeignKey(MedicineOrderHead, on_delete=models.CASCADE, null=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True)
    order_qty = models.IntegerField(default=0, null=True)
    mrp = models.FloatField(default=0, null=True)
    amount = models.FloatField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.head.doctor)

    class Meta:
        db_table = 'medicine_order_detail'


class MedicineOrderBillHead(models.Model):
    invoice_number = models.CharField(max_length=100, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    subtotal = models.FloatField(default=0, null=True)
    discount = models.IntegerField(default=0, null=True)
    shipping = models.FloatField(default=0, null=True)
    pay_amount = models.FloatField(default=0, null=True)
    sgst = models.IntegerField(default=0, null=True, blank=True)
    cgst = models.IntegerField(default=0, null=True, blank=True)
    credit = models.IntegerField(default=0, null=True, blank=True)
    cash = models.IntegerField(default=0, null=True, blank=True)
    online = models.IntegerField(default=0, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.doctor)

    class Meta:
        db_table = 'medicine_order_bill_head'


class MedicineOrderBillDetail(models.Model):
    head = models.ForeignKey(MedicineOrderBillHead, on_delete=models.CASCADE, null=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True)
    record_qty = models.IntegerField(default=0, null=True)
    order_qty = models.IntegerField(default=0, null=True)
    sell_qty = models.IntegerField(default=0, null=True)
    mrp = models.FloatField(default=0, null=True)
    sale_rate = models.IntegerField(default=0, null=True)
    discount = models.IntegerField(default=0, null=True)
    amount = models.FloatField(default=0, null=True)
    hsn = models.IntegerField(default=0, null=True)
    gst = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.head.doctor)

    class Meta:
        db_table = 'medicine_order_bill_detail'
