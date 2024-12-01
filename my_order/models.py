from django.db import models

from doctor.models import Doctor

from medicine.models import Medicine

from store.models import Store


# Create your models here.
class MedicineOrderHead(models.Model):
    invoice_number = models.CharField(max_length=100, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    subtotal = models.FloatField(default=0, null=True)
    discount = models.IntegerField(default=0, null=True)
    shipping = models.FloatField(default=0, null=True)
    pay_amount = models.FloatField(default=0, null=True)
    status = models.IntegerField(help_text='0=pending,1=inprocess,2=packing,3=dispatch,4=out of delivery,5=delivered')
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
    hsn = models.CharField(max_length=10, null=True, blank=True)
    gst = models.IntegerField(default=0, null=True, blank=True)
    taxable_amount = models.FloatField(default=0, null=True)
    tax = models.FloatField(default=0, null=True)
    amount = models.FloatField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.head.doctor)

    class Meta:
        db_table = 'medicine_order_detail'


class MedicineOrderBillHead(models.Model):
    order_id = models.ForeignKey(MedicineOrderHead, on_delete=models.CASCADE, null=True)
    invoice_number = models.CharField(max_length=100, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount = models.IntegerField(default=0, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_without_previous_bill = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    sgst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cgst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    old_credit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    new_credit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cash = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    online = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    extra_cash_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    extra_online_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amount_remark = models.CharField(max_length=100, null=True, blank=True)

    status = models.IntegerField(help_text='0=pending,1=inprocess,2=packing,3=dispatch,4=out of delivery,5=delivered')
    estimate_status = models.IntegerField(default=0, help_text='0=pending,1=complete')
    order_type = models.IntegerField(help_text='1=In state,2=other state,3=bill of supply')
    account_number = models.CharField(max_length=100, null=True, blank=True)
    ifc_number = models.CharField(max_length=100, null=True, blank=True)
    upi_id_number = models.CharField(max_length=100, null=True, blank=True)
    bar_code = models.ImageField(upload_to='bank_account_barcode', null=True, blank=True)
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
    mrp = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount = models.IntegerField(default=0, null=True)
    sale_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    hsn = models.CharField(max_length=10, null=True, blank=True)
    gst = models.IntegerField(default=0, null=True, blank=True)
    taxable_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.head.doctor)

    class Meta:
        db_table = 'medicine_order_bill_detail'


class EstimateMedicineOrderBillHead(models.Model):
    order_id = models.ForeignKey(MedicineOrderHead, on_delete=models.CASCADE, null=True)
    invoice_number = models.CharField(max_length=100, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount = models.IntegerField(default=0, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_without_previous_bill = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    sgst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cgst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    old_credit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    new_credit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cash = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    online = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    extra_cash_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    extra_online_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amount_remark = models.CharField(max_length=100, null=True, blank=True)

    status = models.IntegerField(help_text='0=pending,1=inprocess,2=packing,3=dispatch,4=out of delivery,5=delivered')
    order_type = models.IntegerField(help_text='1=In state,2=other state,3=bill of supply')
    account_number = models.CharField(max_length=100, null=True, blank=True)
    ifc_number = models.CharField(max_length=100, null=True, blank=True)
    upi_id_number = models.CharField(max_length=100, null=True, blank=True)
    bar_code = models.ImageField(upload_to='bank_account_barcode', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.doctor)

    class Meta:
        db_table = 'estimate_medicine_order_bill_head'


class EstimateMedicineOrderBillDetail(models.Model):
    head = models.ForeignKey(EstimateMedicineOrderBillHead, on_delete=models.CASCADE, null=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True)
    record_qty = models.IntegerField(default=0, null=True)
    order_qty = models.IntegerField(default=0, null=True)
    sell_qty = models.IntegerField(default=0, null=True)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount = models.IntegerField(default=0, null=True)
    sale_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    hsn = models.CharField(max_length=10, null=True, blank=True)
    gst = models.IntegerField(default=0, null=True, blank=True)
    taxable_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.head.doctor)

    class Meta:
        db_table = 'estimate_medicine_order_bill_detail'
