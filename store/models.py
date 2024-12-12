from django.db import models
from account.models import User

from medicine.models import Medicine


# Create your models here.
class Store(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        db_table = 'stores'


class MedicineStore(models.Model):
    from_store = models.ForeignKey(Store, related_name='Medicine_from_store', on_delete=models.CASCADE)
    to_store = models.ForeignKey(Store, related_name='Medicine_to_store', on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    qty = models.IntegerField(null=True, blank=True)
    min_medicine_record_qty = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    batch_no = models.CharField(max_length=100, null=True)
    expiry = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.medicine.name)

    class Meta:
        db_table = 'medicine_store'


class MedicineStoreTransactionHistory(models.Model):
    from_store = models.ForeignKey(Store, related_name='Medicine_transfer_history_from_store', on_delete=models.CASCADE)
    to_store = models.ForeignKey(Store, related_name='Medicine_transfer_history_to_store', on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=256, null=True)
    category = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    batch_no = models.CharField(max_length=100, null=True)
    available_qty = models.IntegerField(null=True)
    add_qty = models.IntegerField(null=True, default=0)
    minus_qty = models.IntegerField(null=True, default=0)
    sell_qty = models.IntegerField(null=True, default=0)
    transfer_qty = models.IntegerField(null=True, default=0)
    medicine_manufacture = models.CharField(max_length=256, null=True)
    medicine_expiry = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.medicine_name)

    class Meta:
        db_table = 'medicine_store_transaction_history'
