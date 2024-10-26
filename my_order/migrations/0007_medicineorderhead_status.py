# Generated by Django 5.0.6 on 2024-10-26 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_order', '0006_medicineorderbillhead_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicineorderhead',
            name='status',
            field=models.IntegerField(default=0, help_text='0=pending,1=inprocess,2=packing,3=dispatch,4=out of delivery,5=delivered'),
            preserve_default=False,
        ),
    ]
