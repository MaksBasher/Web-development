# Generated by Django 4.2 on 2023-06-18 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('omg', '0020_product_stock_alter_product_discount_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.CharField(blank=True, default=1, max_length=64, null=True),
        ),
    ]
