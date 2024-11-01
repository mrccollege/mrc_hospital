from django.db import models


# Create your models here.
class PaymentDetail(models.Model):
    account_number = models.CharField(max_length=100, null=True, blank=True)
    ifc_number = models.CharField(max_length=100, null=True, blank=True)
    upi_id_number = models.CharField(max_length=100, null=True, blank=True)
    bar_code = models.ImageField(upload_to='bank_account_barcode', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.account_number) + str(' ') + str(self.ifc_number)

    class Meta:
        db_table = 'payment_detail'
