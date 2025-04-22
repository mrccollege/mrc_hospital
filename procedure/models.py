from django.db import models

from store.models import Store

from patient.models import Patient


# Create your models here.
class CategoryProcedure(models.Model):
    name = models.CharField(max_length=100, null=True)
    desc = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'category_procedure'


class Procedure(models.Model):
    category = models.ForeignKey(CategoryProcedure, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True)
    desc = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'procedure'


class ProcedureBillHead(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount = models.IntegerField(default=0, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    flat_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_without_previous_bill = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    old_credit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    new_credit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cash = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    online = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    extra_cash_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    extra_online_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amount_remark = models.CharField(max_length=100, null=True, blank=True)

    status = models.IntegerField(help_text='0=pending,1=inprocess,2=packing,3=dispatch,4=out of delivery,5=delivered')
    account_number = models.CharField(max_length=100, null=True, blank=True)
    ifc_number = models.CharField(max_length=100, null=True, blank=True)
    upi_id_number = models.CharField(max_length=100, null=True, blank=True)
    bar_code = models.ImageField(upload_to='bank_account_barcode', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.patient)

    class Meta:
        db_table = 'procedure_bill_head'


class ProcedureBillDetail(models.Model):
    head = models.ForeignKey(ProcedureBillHead, on_delete=models.CASCADE, null=True)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    sell_qty = models.IntegerField(default=0, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    from_date = models.DateTimeField(null=True, blank=True)
    to_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.head.patient)

    class Meta:
        db_table = 'procedure_bill_detail'
