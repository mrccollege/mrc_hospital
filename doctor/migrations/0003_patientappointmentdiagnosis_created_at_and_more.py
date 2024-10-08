# Generated by Django 5.0.6 on 2024-09-23 09:30

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_remove_otherassociatescomplaints_bleeding_and_more'),
        ('previous_treatment', '0002_alter_previoustreatment_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientappointmentdiagnosis',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patientappointmentdiagnosis',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.CreateModel(
            name='PreviousTreatmentAppointmentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('head', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='doctor.patientappointmenthead')),
                ('remark', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='previous_treatment.previoustreatment')),
            ],
            options={
                'db_table': 'previous_treatment_appointment_details',
            },
        ),
    ]
