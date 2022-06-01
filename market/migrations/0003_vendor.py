# Generated by Django 4.0.4 on 2022-05-09 15:36

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('market', '0002_alter_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=11, null=True)),
                ('about', models.CharField(blank=True, max_length=255, null=True)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('account_visit', models.IntegerField(default=0)),
                ('account_engaged', models.IntegerField(default=0)),
                ('is_verified', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=datetime.datetime.now)),
                ('follower', models.ManyToManyField(blank=True, related_name='vendor_follower_list', to=settings.AUTH_USER_MODEL)),
                ('following', models.ManyToManyField(blank=True, related_name='vendor_following_list', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
