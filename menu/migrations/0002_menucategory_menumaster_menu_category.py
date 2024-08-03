# Generated by Django 5.0.6 on 2024-07-30 03:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_title', models.CharField(max_length=100, null=True)),
                ('cat_desc', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'menu_category',
            },
        ),
        migrations.AddField(
            model_name='menumaster',
            name='menu_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='menu.menucategory'),
        ),
    ]