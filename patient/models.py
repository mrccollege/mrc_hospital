from django.db import models

from account.models import User

from medicine.models import Medicine

from store.models import Store


class SocialMediaReference(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'social_media_reference'


class OtherReference(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'other_reference'


class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    social_media = models.ForeignKey(SocialMediaReference, on_delete=models.CASCADE, null=True, blank=True)
    other_reference = models.ForeignKey(OtherReference, on_delete=models.CASCADE, null=True, blank=True)
    patient_code = models.CharField(max_length=20, null=True, blank=True)
    reference_by_patient = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        db_table = 'patient'


class PatientMedicineBillHead(models.Model):
    invoice_number = models.CharField(max_length=100, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
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
    final_bill_status = models.IntegerField(default=0, help_text='0=pending,1=complete')
    order_type = models.IntegerField(help_text='1=In state,2=other state,3=bill of supply')
    account_number = models.CharField(max_length=100, null=True, blank=True)
    ifc_number = models.CharField(max_length=100, null=True, blank=True)
    upi_id_number = models.CharField(max_length=100, null=True, blank=True)
    bar_code = models.ImageField(upload_to='bank_account_barcode', null=True, blank=True)
    state_code = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.doctor)

    class Meta:
        db_table = 'patient_medicine_bill_head'


class PatientMedicineBillDetail(models.Model):
    head = models.ForeignKey(PatientMedicineBillHead, on_delete=models.CASCADE, null=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True)
    batch_no = models.CharField(max_length=50, null=True, blank=True)
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
        db_table = 'patient_medicine_bill_detail'


class PatientMedicineUnregisteredBillHead(models.Model):
    head = models.ForeignKey(PatientMedicineBillHead, related_name='Patient_headUnregisteredBillHead',on_delete=models.CASCADE, null=True)
    invoice_number = models.CharField(max_length=100, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
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
    final_bill_status = models.IntegerField(default=0, help_text='0=pending,1=complete')
    order_type = models.IntegerField(help_text='1=In state,2=other state,3=bill of supply')
    account_number = models.CharField(max_length=100, null=True, blank=True)
    ifc_number = models.CharField(max_length=100, null=True, blank=True)
    upi_id_number = models.CharField(max_length=100, null=True, blank=True)
    bar_code = models.ImageField(upload_to='bank_account_barcode', null=True, blank=True)
    state_code = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.doctor)

    class Meta:
        db_table = 'patient_medicine_unregistered_bill_head'


class PatientMedicineUnregisteredBillDetail(models.Model):
    head = models.ForeignKey(PatientMedicineUnregisteredBillHead, on_delete=models.CASCADE, null=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True)
    batch_no = models.CharField(max_length=50, null=True, blank=True)
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
        db_table = 'patient_medicine_unregistered_bill_detail'


class PatientEstimateMedicineBillHead(models.Model):
    head = models.ForeignKey(PatientMedicineBillHead, on_delete=models.CASCADE, null=True)
    invoice_number = models.CharField(max_length=100, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
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
    state_code = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.doctor)

    class Meta:
        db_table = 'patient_estimate_medicine_bill_head'


class PatientEstimateMedicineBillDetail(models.Model):
    head = models.ForeignKey(PatientEstimateMedicineBillHead, on_delete=models.CASCADE, null=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True)
    batch_no = models.CharField(max_length=50, null=True, blank=True)
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
        db_table = 'patient_estimate_medicine_bill_detail'
