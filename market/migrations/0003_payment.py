# Generated by Django 4.0.4 on 2022-11-08 14:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('ref', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('verified', models.BooleanField()),
                ('date_posted', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'ordering': ['-date_posted'],
            },
        ),
    ]