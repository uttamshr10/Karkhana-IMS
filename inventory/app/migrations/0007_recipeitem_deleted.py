# Generated by Django 5.0.4 on 2024-09-04 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_recipe_inventory_remove_recipe_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipeitem',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
