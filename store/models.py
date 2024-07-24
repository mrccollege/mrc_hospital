from django.db import models
from account.models import User

from medicine.models import Medicine


# Create your models here.
class Store(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    type = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        db_table = 'stores'


class MainStoreMedicine(models.Model):
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    qty = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.medicine.medicine_name)

    class Meta:
        db_table = 'main_store_medicine'


class MainStoreMedicineTransaction(models.Model):
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    medicine_name = models.CharField(max_length=500, null=True)
    qty = models.IntegerField(null=True)
    medicine_manufacturer = models.CharField(max_length=500, null=True)
    medicine_expiry = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.medicine_name)

    class Meta:
        db_table = 'main_store_medicine_transaction'
