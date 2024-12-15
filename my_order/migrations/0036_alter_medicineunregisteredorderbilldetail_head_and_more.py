# Generated by Django 5.0.6 on 2024-12-15 06:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_order', '0035_medicineunregisteredorderbilldetail_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicineunregisteredorderbilldetail',
            name='head',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='my_order.medicineunregisteredorderbillhead'),
        ),
        migrations.AlterField(
            model_name='medicineunregisteredorderbillhead',
            name='order_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='UnregisteredOrderBillHead', to='my_order.medicineorderhead'),
        ),
    ]