# Generated by Django 5.0.4 on 2024-09-20 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_standardinventory_alter_inventory_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='standardinventory',
            name='price_per_unit',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='standardinventory',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
