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


class MedicineStore(models.Model):
    from_store = models.ForeignKey(Store, related_name='Medicine_from_store', on_delete=models.PROTECT)
    to_store = models.ForeignKey(Store, related_name='Medicine_to_store', on_delete=models.PROTECT)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    qty = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.medicine.medicine_name)

    class Meta:
        db_table = 'medicine_store'


class MedicineStoreTransactionHistory(models.Model):
    from_store = models.ForeignKey(Store, related_name='Medicine_transfer_history_from_store', on_delete=models.PROTECT)
    to_store = models.ForeignKey(Store, related_name='Medicine_transfer_history_to_store', on_delete=models.PROTECT)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    medicine_name = models.CharField(max_length=500, null=True)
    qty = models.IntegerField(null=True)
    medicine_manufacturer = models.CharField(max_length=500, null=True)
    medicine_expiry = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.medicine_name)

    class Meta:
        db_table = 'medicine_store_transaction_history'


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


class MainToMiniStoreMedicine(models.Model):
    from_store = models.ForeignKey(Store, related_name='from_store', on_delete=models.PROTECT)
    to_store = models.ForeignKey(Store, related_name='to_store', on_delete=models.PROTECT)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    qty = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.medicine.medicine_name)

    class Meta:
        db_table = 'main_to_mini_store_medicine'


class MiniToMiniStoreMedicine(models.Model):
    from_store = models.ForeignKey(Store, related_name='mini_to_mini_from_store', on_delete=models.PROTECT)
    to_store = models.ForeignKey(Store, related_name='mini_to_mini_to_store', on_delete=models.PROTECT)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    qty = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.medicine.medicine_name)

    class Meta:
        db_table = 'mini_to_mini_store_medicine'


class MainToMiniStoreMedicineTransaction(models.Model):
    from_store = models.ForeignKey(Store, related_name='main_to_mini_transaction_from_store', on_delete=models.PROTECT)
    to_store = models.ForeignKey(Store, related_name='main_to_mini_transaction_to_store', on_delete=models.PROTECT)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    medicine_name = models.CharField(max_length=500, null=True)
    qty = models.IntegerField(null=True)
    medicine_manufacturer = models.CharField(max_length=500, null=True)
    medicine_expiry = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.medicine.medicine_name)

    class Meta:
        db_table = 'main_to_mini_store_medicine_transaction'


class MiniToMiniStoreMedicineTransaction(models.Model):
    from_store = models.ForeignKey(Store, related_name='mini_to_mini_transaction_from_store', on_delete=models.PROTECT)
    to_store = models.ForeignKey(Store, related_name='mini_to_mini_transaction_to_store', on_delete=models.PROTECT)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    medicine_name = models.CharField(max_length=500, null=True)
    qty = models.IntegerField(null=True)
    medicine_manufacturer = models.CharField(max_length=500, null=True)
    medicine_expiry = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.medicine.medicine_name)

    class Meta:
        db_table = 'mini_to_mini_store_medicine_transaction'
