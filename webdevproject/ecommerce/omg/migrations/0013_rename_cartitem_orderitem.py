# Generated by Django 4.2 on 2023-05-08 02:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('omg', '0012_alter_brand_options_alter_discount_options_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CartItem',
            new_name='OrderItem',
        ),
    ]