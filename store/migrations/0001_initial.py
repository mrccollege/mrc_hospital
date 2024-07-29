# Generated by Django 5.0.6 on 2024-07-29 04:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medicine', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'stores',
            },
        ),
        migrations.CreateModel(
            name='MiniToMiniStoreMedicineTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine_name', models.CharField(max_length=500, null=True)),
                ('qty', models.IntegerField(null=True)),
                ('medicine_manufacturer', models.CharField(max_length=500, null=True)),
                ('medicine_expiry', models.DateField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='medicine.medicine')),
                ('from_store', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mini_to_mini_transaction_from_store', to='store.store')),
                ('to_store', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mini_to_mini_transaction_to_store', to='store.store')),
            ],
            options={
                'db_table': 'mini_to_mini_store_medicine_transaction',
            },
        ),
        migrations.CreateModel(
            name='MiniToMiniStoreMedicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='medicine.medicine')),
                ('from_store', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mini_to_mini_from_store', to='store.store')),
                ('to_store', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mini_to_mini_to_store', to='store.store')),
            ],
            options={
                'db_table': 'mini_to_mini_store_medicine',
            },
        ),
        migrations.CreateModel(
            name='MedicineStoreTransactionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine_name', models.CharField(max_length=500, null=True)),
                ('qty', models.IntegerField(null=True)),
                ('medicine_manufacturer', models.CharField(max_length=500, null=True)),
                ('medicine_expiry', models.DateField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='medicine.medicine')),
                ('from_store', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Medicine_transfer_history_from_store', to='store.store')),
                ('to_store', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Medicine_transfer_history_to_store', to='store.store')),
            ],
            options={
                'db_table': 'medicine_store_transaction_history',
            },
        ),
        migrations.CreateModel(
            name='MedicineStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='medicine.medicine')),
                ('from_store', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Medicine_from_store', to='store.store')),
                ('to_store', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Medicine_to_store', to='store.store')),
            ],
            options={
                'db_table': 'medicine_store',
            },
        ),
        migrations.CreateModel(
            name='MainToMiniStoreMedicineTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine_name', models.CharField(max_length=500, null=True)),
                ('qty', models.IntegerField(null=True)),
                ('medicine_manufacturer', models.CharField(max_length=500, null=True)),
                ('medicine_expiry', models.DateField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='medicine.medicine')),
                ('from_store', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='main_to_mini_transaction_from_store', to='store.store')),
                ('to_store', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='main_to_mini_transaction_to_store', to='store.store')),
            ],
            options={
                'db_table': 'main_to_mini_store_medicine_transaction',
            },
        ),
        migrations.CreateModel(
            name='MainToMiniStoreMedicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='medicine.medicine')),
                ('from_store', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='from_store', to='store.store')),
                ('to_store', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='to_store', to='store.store')),
            ],
            options={
                'db_table': 'main_to_mini_store_medicine',
            },
        ),
        migrations.CreateModel(
            name='MainStoreMedicineTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine_name', models.CharField(max_length=500, null=True)),
                ('qty', models.IntegerField(null=True)),
                ('medicine_manufacturer', models.CharField(max_length=500, null=True)),
                ('medicine_expiry', models.DateField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.store')),
            ],
            options={
                'db_table': 'main_store_medicine_transaction',
            },
        ),
        migrations.CreateModel(
            name='MainStoreMedicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='medicine.medicine')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.store')),
            ],
            options={
                'db_table': 'main_store_medicine',
            },
        ),
    ]
