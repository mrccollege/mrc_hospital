# Generated by Django 5.0.6 on 2024-07-24 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicine',
            name='medicine_qty',
        ),
    ]
