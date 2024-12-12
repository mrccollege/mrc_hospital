# Generated by Django 5.0.6 on 2024-12-12 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_medicinestore_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicinestore',
            name='min_medicine_record_qty',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='medicinestore',
            name='expiry',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='medicinestore',
            name='qty',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
