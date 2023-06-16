import csv
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from .models import *
from django.db.models import Q, F


# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "date"]
    list_per_page = 15


class ProductReviewInline(admin.TabularInline):
    model = ProductReview


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "vendor", "price", "product_purchase", "date_posted"]
    search_fields = ["name", "vendor__user__username"]
    list_filter = ['vendor', 'date_posted']
    actions = ['apply_discount', "remove_discount", "export_products"]
    list_per_page = 15
    inlines = [ProductReviewInline, ProductImageInline]

    def apply_discount(self, request, queryset):
        if 'apply' in request.POST:
            queryset.update(price=F('price') * float(0.9))

            self.message_user(request,
                              "Applied discount on {} product".format([i.name for i in queryset]))
            return HttpResponseRedirect(request.get_full_path())

        return render(request,
                      'market/test.html',
                      context={'orders': queryset})

    apply_discount.short_description = 'Apply 10%% discount'

    def remove_discount(self, request, queryset):
        queryset.update(price=F('price') / float(0.9))
        self.message_user(request,
                          "Removed discount on {} product".format([i.name for i in queryset]))

    remove_discount.short_description = 'Remove 10%% discount'

    def export_products(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'
        writer = csv.writer(response)
        writer.writerow(['id', 'name', 'price', 'description',
                         'category', "product_purchase", 'vendor', "date_posted"])
        products = queryset.values_list('id', 'name', 'price', 'description',
                                        'category__name', "product_purchase", 'vendor__user__username', "date_posted")
        for product in products:
            writer.writerow(product)
        return response

    export_products.short_description = 'Export to csv'


class VendorReviewInline(admin.TabularInline):
    model = VendorReview


class VendorAdmin(admin.ModelAdmin):
    list_display = ["user", "phone_number", "location", "date_joined", "is_verified"]
    list_filter = ['date_joined', "is_verified"]
    search_fields = ["user__username", "full_name"]
    list_per_page = 15
    filter_horizontal = ['following', "follower"]
    inlines = [VendorReviewInline]


class VendorReviewAdmin(admin.ModelAdmin):
    list_display = ["vendor", "sender", "date_posted"]
    list_per_page = 15


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "date_posted"]
    search_fields = ["product__name"]


class CheckoutAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "quantity", "date_posted", "complete"]
    list_filter = ['date_posted', "complete", 'user']
    search_fields = ["user__username", "product__name"]
    list_per_page = 15


class MembershipInline(admin.TabularInline):
    model = Order.order_item.through


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'vendor', 'date_posted']
    search_fields = ["user__username"]
    filter_horizontal = ['order_item']
    list_filter = ['user', "vendor", 'date_posted']
    list_per_page = 15
    # inlines = [
    #     MembershipInline,
    # ]
    # exclude = ('order_item',)


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["customer_info", "product", "date_added"]
    list_per_page = 15


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Checkout, CheckoutAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(VendorReview, VendorReviewAdmin)
