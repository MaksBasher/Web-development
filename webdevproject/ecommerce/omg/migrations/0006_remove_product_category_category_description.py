# Generated by Django 4.2 on 2023-05-07 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('omg', '0005_alter_inventory_options_alter_news_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product_category',
            name='category_description',
        ),
    ]
