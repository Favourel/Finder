import secrets
from django.db import models
from django.conf import settings
from datetime import datetime, date
from django.shortcuts import reverse
import uuid
from .paystack import Paystack


# Create your models here.


class Vendor(models.Model):
    EDUCATION_TYPES = (
        (1, "B.Sc."), (2, "M.Sc."), (3, "M.A."), (4, "M.Sc."), (5, "LLB"), (6, "Others"),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, default="")
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    about = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    education = models.IntegerField(choices=EDUCATION_TYPES, default=6)
    follower = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='vendor_follower_list')
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='vendor_following_list')
    account_visit = models.IntegerField(default=0)
    account_engaged = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=datetime.now)
    twitter_url = models.URLField(default="")
    instagram_url = models.URLField(default="")
    skills = models.CharField(max_length=20, default="")
    paystack_public_key = models.CharField(max_length=100, null=True, blank=True)
    paystack_secret_key = models.CharField(max_length=100, null=True, blank=True)
    paid_until = models.DateField(
        null=True,
        blank=True
    )

    def set_paid_until(self, date_or_timestamp):
        if isinstance(date_or_timestamp, int):
            # input date as timestamp integer
            paid_until = date.fromtimestamp(date_or_timestamp)
        elif isinstance(date_or_timestamp, str):
            # input date as timestamp string
            paid_until = date.fromtimestamp(int(date_or_timestamp))
        else:
            paid_until = date_or_timestamp

        self.paid_until = paid_until
        self.save()

    def has_paid(
            self,
            current_date=datetime.now()
    ):
        if self.paid_until is None:
            return False

        return current_date < self.paid_until

    def __str__(self):
        return f"{self.user}"


class Category(models.Model):
    name = models.CharField(max_length=100, default="Select Category")
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name

    @staticmethod
    def getAllCategory():
        return Category.objects.all()


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    image = models.ImageField(default='2placeholder_test_b9l9NT5.png', upload_to='product_images')
    description = models.TextField(default="")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_purchase = models.IntegerField(default=0)
    vendor = models.ForeignKey(Vendor, null=True, blank=True, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=datetime.now)
    date_updated = models.DateTimeField(auto_now=True)
    delivery_period = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"pk": self.id})

    @staticmethod
    def getProductByFilter(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.objects.all()

    def amount(self):
        total = self.price * self.product_purchase
        return total


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(default='2placeholder_test_b9l9NT5.png', upload_to='product_images')
    date_posted = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.image}"


class Checkout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    complete = models.BooleanField(default=False, null=True, blank=True)
    date_posted = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.user}: {self.quantity} of {self.product}'

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=30)
    order_item = models.ManyToManyField(Checkout, related_name="order_item")
    vendor = models.ForeignKey(Vendor, blank=True, null=True, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.user}'

    @property
    def total_order_item_price(self):
        total = self.order_item.all()
        total_price = sum([i.get_total for i in total])
        return total_price


class ProductReview(models.Model):
    customer_info = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    date_added = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.customer_info.username} comment'


class Payment(models.Model):
    amount = models.IntegerField()
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField()
    date_posted = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ["-date_posted"]

    def __str__(self):
        return f"Payment: {self.amount}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self):
        return self.amount * 100

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result["amount"] / 100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False
