# Generated by Django 4.0.4 on 2022-05-09 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0006_vendor_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='paid_until',
            field=models.DateField(blank=True, null=True),
        ),
    ]
