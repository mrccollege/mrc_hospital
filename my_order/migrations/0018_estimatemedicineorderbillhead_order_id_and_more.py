# Generated by Django 5.0.6 on 2024-10-31 07:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_order', '0017_remove_medicineorderdetail_invoice_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='estimatemedicineorderbillhead',
            name='order_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='my_order.medicineorderhead'),
        ),
        migrations.AddField(
            model_name='medicineorderbillhead',
            name='order_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='my_order.medicineorderhead'),
        ),
    ]