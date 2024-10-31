# Generated by Django 5.0.6 on 2024-10-31 06:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0003_patientappointmentdiagnosis_created_at_and_more'),
        ('medicine', '0004_medicine_video_link'),
        ('my_order', '0014_alter_medicineorderbilldetail_amount_and_more'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstimateMedicineOrderBillHead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=100, null=True)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('discount', models.IntegerField(default=0, null=True)),
                ('shipping', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('pay_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('sgst', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cgst', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('old_credit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('credit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cash', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('online', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.IntegerField(help_text='0=pending,1=inprocess,2=packing,3=dispatch,4=out of delivery,5=delivered')),
                ('order_type', models.IntegerField(help_text='1=In state,2=other state,3=bill of supply')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='doctor.doctor')),
                ('store', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.store')),
            ],
            options={
                'db_table': 'estimate_medicine_order_bill_head',
            },
        ),
        migrations.CreateModel(
            name='EstimateMedicineOrderBillDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_qty', models.IntegerField(default=0, null=True)),
                ('order_qty', models.IntegerField(default=0, null=True)),
                ('sell_qty', models.IntegerField(default=0, null=True)),
                ('mrp', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('discount', models.IntegerField(default=0, null=True)),
                ('sale_rate', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('hsn', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('gst', models.IntegerField(default=0, null=True)),
                ('taxable_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('medicine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='medicine.medicine')),
                ('head', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='my_order.estimatemedicineorderbillhead')),
            ],
            options={
                'db_table': 'estimate_medicine_order_bill_detail',
            },
        ),
    ]
