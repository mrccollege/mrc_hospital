# Generated by Django 5.0.6 on 2024-11-01 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(blank=True, max_length=100, null=True)),
                ('ifc_number', models.CharField(blank=True, max_length=100, null=True)),
                ('upi_id_number', models.CharField(blank=True, max_length=100, null=True)),
                ('bar_code', models.ImageField(blank=True, null=True, upload_to='bank_account_barcode')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'payment_detail',
            },
        ),
    ]
