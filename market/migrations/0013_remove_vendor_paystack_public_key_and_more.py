# Generated by Django 4.0.4 on 2022-11-30 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0012_vendor_withdrawal_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='paystack_public_key',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='paystack_secret_key',
        ),
    ]
