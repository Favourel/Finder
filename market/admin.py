from django.contrib import admin
from .models import *

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "date"]


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "vendor", "price", "date_posted"]
    search_fields = ["name", "vendor"]


class VendorAdmin(admin.ModelAdmin):
    list_display = ["user", "phone_number", "location", "date_joined", "is_verified"]


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "date_posted"]


class CheckoutAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "date_posted", "complete"]


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["customer_info", "product", "date_added"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Checkout, CheckoutAdmin)
