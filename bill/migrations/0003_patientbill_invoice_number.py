# Generated by Django 5.0.6 on 2024-08-09 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0002_patientbill_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientbill',
            name='invoice_number',
            field=models.CharField(max_length=100, null=True),
        ),
    ]