# Generated by Django 5.0.6 on 2024-08-07 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_remove_patientappointment_pulses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientappointment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]