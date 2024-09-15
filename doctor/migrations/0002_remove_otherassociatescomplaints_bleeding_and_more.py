# Generated by Django 5.0.6 on 2024-09-15 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otherassociatescomplaints',
            name='bleeding',
        ),
        migrations.AddField(
            model_name='patientmedicine',
            name='dose',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='patientmedicine',
            name='dose_with',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='patientmedicine',
            name='interval',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
