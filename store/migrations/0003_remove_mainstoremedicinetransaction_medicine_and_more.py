# Generated by Django 5.0.6 on 2024-07-24 09:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0002_remove_medicine_medicine_qty'),
        ('store', '0002_mainstoremedicinetransaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainstoremedicinetransaction',
            name='medicine',
        ),
        migrations.AddField(
            model_name='mainstoremedicinetransaction',
            name='medicine_expiry',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='mainstoremedicinetransaction',
            name='medicine_manufacturer',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='mainstoremedicinetransaction',
            name='medicine_name',
            field=models.CharField(max_length=500, null=True),
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
