# Generated by Django 4.2.16 on 2025-01-06 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_rename_title_product_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='name',
            new_name='p_name',
        ),
    ]
