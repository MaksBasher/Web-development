# Generated by Django 4.2 on 2023-05-19 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('omg', '0014_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]