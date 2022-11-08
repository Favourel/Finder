from django.contrib import admin
from .models import *

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "date"]


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "vendor", "price", "product_purchase", "date_posted"]
    search_fields = ["name", "vendor"]


class VendorAdmin(admin.ModelAdmin):
    list_display = ["user", "phone_number", "location", "date_joined", "is_verified"]


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "date_posted"]


class CheckoutAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "quantity", "date_posted", "complete"]


class MembershipInline(admin.TabularInline):
    model = Order.order_item.through


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_posted']
    search_fields = ["user"]
    filter_horizontal = ['order_item']
    # inlines = [
    #     MembershipInline,
    # ]
    # exclude = ('order_item',)


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["customer_info", "product", "date_added"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Checkout, CheckoutAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
