# Generated by Django 5.0.6 on 2024-09-23 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_order', '0002_alter_medicineorderhead_pay_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicineorderdetail',
            name='amount',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='medicineorderdetail',
            name='mrp',
            field=models.FloatField(default=0, null=True),
        ),
    ]