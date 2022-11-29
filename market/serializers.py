from rest_framework import serializers
from .models import Order, Checkout, Product, ProductImage
from django.contrib.humanize.templatetags.humanize import intcomma
from rest_framework.reverse import reverse


class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    image = serializers.ImageField(read_only=True)


class VendorPublicSerializer(serializers.Serializer):
    user = UserPublicSerializer(read_only=True)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):
    edited_price = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    vendor = VendorPublicSerializer(read_only=True)
    vendor_url = serializers.SerializerMethodField(read_only=True)
    times = serializers.SerializerMethodField(read_only=True)
    products_images = ProductImageSerializer(source="productimage_set", read_only=True, many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "url",
            "name",
            "price",
            "edited_price",
            "image",
            "product_purchase",
            "vendor",
            "vendor_url",
            "products_images",
            "rating_count",
            "times",
        ]

    @classmethod
    def get_edited_price(cls, obj):
        return f"${intcomma(obj.price)}0"

    def get_url(self, obj):
        request = self.context.get("request")
        return reverse("product-detail", kwargs={"pk": obj.id}, request=request)

    def get_vendor_url(self, obj):
        request = self.context.get("request")
        return reverse("vendor", kwargs={"username": obj.vendor.user}, request=request)

    @classmethod
    def get_times(cls, obj):
        range_round = range(round(obj.rating_count))
        print(range(round(obj.rating_count)))
        return str(range_round)


class OrderSerializer(serializers.ModelSerializer):
    total_order_item_price = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    user = UserPublicSerializer(read_only=True)
    # order_item = serializers.SerializerMethodField(read_only=True)
    vendor = VendorPublicSerializer(read_only=True)
    order_item_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "user",
            "username",
            "transaction_id",
            "order_item",
            "order_item_data",
            "vendor",
            "ordered",
            "total_order_item_price",
            "date_posted",
        ]

    @classmethod
    def get_total_order_item_price(cls, obj):
        total = obj.order_item.all()
        total_price = sum([i.get_total for i in total])
        return f"${intcomma(total_price)}0"

    @classmethod
    def get_username(cls, obj):
        return obj.user.username

    @classmethod
    def get_order_item_data(cls, obj):
        all_order = obj.order_item.all()
        order_item_list = [str(order) for order in all_order]
        return order_item_list
