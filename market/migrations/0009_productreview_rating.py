# Generated by Django 4.0.4 on 2022-11-28 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0008_alter_productimage_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(blank=True, choices=[(1, '★☆☆☆☆ (1/5)'), (2, '★★☆☆☆ (2/5)'), (3, '★★★☆☆ (3/5)'), (4, '★★★★☆ (4/5)'), (5, '★★★★★ (5/5)')], null=True),
        ),
    ]
