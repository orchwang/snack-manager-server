# Generated by Django 4.2.9 on 2024-01-08 08:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0003_alter_snack_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='snacks_cart',
            new_name='carts',
        ),
    ]