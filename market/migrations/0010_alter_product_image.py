# Generated by Django 4.0.4 on 2022-05-09 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0009_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='2placeholder_test_b9l9NT5.png', upload_to='product_images'),
        ),
    ]
