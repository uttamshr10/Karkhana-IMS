# Generated by Django 5.0.4 on 2024-09-22 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_inventory_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='location',
        ),
    ]
