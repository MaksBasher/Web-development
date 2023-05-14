# Generated by Django 4.2 on 2023-05-07 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('omg', '0010_remove_product_inventory_id_product_stock_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stock_status',
            field=models.IntegerField(choices=[(0, 'Out of Stock'), (1, 'In Stock')], default=0),
        ),
    ]