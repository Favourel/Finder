from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime
from market.models import Product, Checkout

# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    about = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(default='profile_picture/download_EPBN0x6.jpg', upload_to='profile_picture')
    location = models.CharField(max_length=50, null=True, blank=True)

    follower = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='follower_list')
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='following_list')

    account_visit = models.IntegerField(default=0)
    account_engaged = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    post_notification = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_notify')


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        (1, "Order"), (2, "follow"), (3, "Post Notification"),
                          )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,
                             related_name="noti_to_user")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True,
                               on_delete=models.CASCADE, related_name="noti_from_user")

    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Checkout, blank=True)

    date_posted = models.DateTimeField(default=datetime.now)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} notification'
