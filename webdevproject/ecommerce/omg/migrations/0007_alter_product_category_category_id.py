# Generated by Django 4.2 on 2023-05-07 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('omg', '0006_remove_product_category_category_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_category',
            name='category_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]