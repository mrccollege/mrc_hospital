# Generated by Django 5.0.6 on 2024-12-01 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_order', '0031_medicineorderbillhead_amount_remark_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='estimatemedicineorderbillhead',
            name='amount_remark',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='estimatemedicineorderbillhead',
            name='extra_cash_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='estimatemedicineorderbillhead',
            name='extra_online_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]