# Generated by Django 4.2.1 on 2023-07-25 03:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_remove_product_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='images',
        ),
    ]
