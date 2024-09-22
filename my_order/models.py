from django.db import models

from doctor.models import Doctor

from medicine.models import Medicine


# Create your models here.
class MedicineOrderHead(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    discount = models.IntegerField(default=0, null=True)
    amount = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.doctor.user.username)

    class Meta:
        db_table = 'medicine_order_head'


class MedicineOrderDetail(models.Model):
    head = models.ForeignKey(MedicineOrderHead, on_delete=models.CASCADE, null=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True)
    order_qty = models.IntegerField(default=0, null=True)
    mrp = models.IntegerField(default=0, null=True)
    amount = models.IntegerField(default=0, null=True)
    discount = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.head.doctor.user.username)

    class Meta:
        db_table = 'medicine_order_detail'
