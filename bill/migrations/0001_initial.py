# Generated by Django 5.0.6 on 2024-08-09 04:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medicine', '0002_medicine_medicine_price'),
        ('patient', '0005_remove_patient_patient_bp_max_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientBill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='patient.patient')),
            ],
            options={
                'db_table': 'patient_bill',
            },
        ),
        migrations.CreateModel(
            name='PatientBillDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine_qty', models.IntegerField(null=True)),
                ('medicine_sell_qty', models.IntegerField(null=True)),
                ('medicine_price', models.IntegerField(null=True)),
                ('medicine_sell_price', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('medicine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='medicine.medicine')),
                ('patient_bill', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='bill.patientbill')),
            ],
            options={
                'db_table': 'patient_bill_detail',
            },
        ),
    ]