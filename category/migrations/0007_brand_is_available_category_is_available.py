# Generated by Django 4.2.1 on 2023-07-24 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0006_alter_brand_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='category',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]