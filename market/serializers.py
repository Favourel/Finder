from rest_framework import serializers
from .models import Order, Checkout
from django.contrib.humanize.templatetags.humanize import intcomma


class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)


class VendorPublicSerializer(serializers.Serializer):
    user = UserPublicSerializer(read_only=True)


class CheckoutSerializer(serializers.ModelSerializer):
    # orders = serializers.ManyRelatedField(child_relation="order", read_only=True)

    class Meta:
        model = Checkout
        fields = [
            "id",
            "user",
            "product",
            "quantity",
            "complete",
            "date_posted",
        ]


class OrderSerializer(serializers.ModelSerializer):
    total_order_item_price = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    user = UserPublicSerializer(read_only=True)
    # order_item = serializers.SerializerMethodField(read_only=True)
    # order_item = CheckoutSerializer(read_only=True, many=True)
    vendor = VendorPublicSerializer(read_only=True)
    order_item_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
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

    def get_total_order_item_price(self, obj):
        total = obj.order_item.all()
        total_price = sum([i.get_total for i in total])
        return f"${intcomma(total_price)}0"

    def get_username(self, obj):
        return obj.user.username

    def get_order_item_data(self, obj):
        all_order = obj.order_item.all()
        print([str(i) for i in all_order])
        order_item_list = [str(i) for i in all_order]
        return order_item_list
