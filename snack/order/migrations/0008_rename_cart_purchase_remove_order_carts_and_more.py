# Generated by Django 4.2.9 on 2024-01-12 06:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0007_alter_snackreaction_snack'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cart',
            new_name='Purchase',
        ),
        migrations.RemoveField(
            model_name='order',
            name='carts',
        ),
        migrations.AddField(
            model_name='order',
            name='purchases',
            field=models.ManyToManyField(through='order.Purchase', to='order.snack'),
        ),
    ]
