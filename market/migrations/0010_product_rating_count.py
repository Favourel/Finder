# Generated by Django 4.0.4 on 2022-11-28 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0009_productreview_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating_count',
            field=models.FloatField(default=0),
        ),
    ]
