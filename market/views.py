from abc import ABC

from django.shortcuts import render, reverse, get_object_or_404, redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, Vendor, ProductImage, Checkout, ProductReview, Order, Payment
from django.db.models import Q, F, Min, Max
from users.models import User, Notification
import datetime
from .forms import ProductForm, CategoryField, ImageField, ReviewBox, ImageFormSet
from django.views.generic import UpdateView, FormView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms.models import modelformset_factory
from django.conf import settings
import json
from .middlewares.market_middleware import checkout_middleware
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductSerializer
from statistics import mean
from .filters import ProductPriceFilter
import os


# Create your views here.
def total_cart_items(request):
    check_out_list = Checkout.objects.filter(user=request.user, complete=False)
    get_cart_items = sum([item.quantity for item in check_out_list])
    return get_cart_items


def home(request):
    categories = Category.objects.all()
    products = Product.objects.all().order_by("-id")[:4]

    context = {
        "categories": categories,
        "products": products,
        "product_count": Product.objects.all().count,
        "users_count": User.objects.all().count,
        "vendors_count": Vendor.objects.all().count
    }
    return render(request, "market/home.html", context)


@login_required
def market_view(request):
    notification = Notification.objects.filter(user=request.user, is_seen=False).order_by("-id")[:10]
    notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()
    categories = Category.objects.all()
    product_list = Product.objects.all().order_by("-product_purchase")
    maximum_price = Product.objects.all().aggregate(Max("price"))
    half_max_price = maximum_price["price__max"] / 2

    price_filter = ProductPriceFilter(request.GET, queryset=product_list)
    product_list = price_filter.qs

    paginator = Paginator(product_list, 5)
    page = request.GET.get('page', 1)

    try:
        product_list = paginator.page(page)
    except PageNotAnInteger:
        product_list = paginator.page(1)
    except EmptyPage:
        product_list = paginator.page(paginator.num_pages)

    page_list = product_list.paginator.page_range

    if request.GET.get('ratings'):
        query = request.GET.get('ratings')
        lookup = Q(rating_count=query)
        result = Product.objects.filter(lookup).distinct()
        price_filter = ProductPriceFilter(request.GET, queryset=result)
        result = price_filter.qs

        return render(request, 'market/market.html', {"products": result,
                                                      # "page_list": page_list,
                                                      "price_filter": price_filter,
                                                      "categories": categories,
                                                      "maximum_price": maximum_price,
                                                      "half_max_price": half_max_price,
                                                      "product": product_list,
                                                      "rating_query": query,
                                                      "notification_count": notification_count,
                                                      "notification": notification,
                                                      "get_cart_items": total_cart_items(request)
                                                      })

    if request.GET.get('low-high-price'):
        query = request.GET.get('low-high-price')
        result = Product.objects.all().order_by(f"{query}")
        price_filter = ProductPriceFilter(request.GET, queryset=result)
        product_list = price_filter.qs

        context = {"products": result,
                   # "page_list": page_list,
                   "price_filter": price_filter,
                   "categories": categories,
                   "maximum_price": maximum_price,
                   "half_max_price": half_max_price,
                   "product": product_list,
                   "rating_query": query,
                   "notification_count": notification_count,
                   "notification": notification,
                   "get_cart_items": total_cart_items(request)
                   }

        return render(request, 'market/market.html', context)

    if request.GET.get('category_id'):
        filterProduct = Product.getProductByFilter(request.GET['category_id']).order_by('-id')
        filter_category_product = filterProduct.all().order_by('-product_purchase')
        price_filter = ProductPriceFilter(request.GET, queryset=filter_category_product)
        result = price_filter.qs
        maximum_price = Product.objects.all().aggregate(Max("price"))
        half_max_price = maximum_price["price__max"] / 2

        return render(request, 'market/market.html', {"products": result,
                                                      # "page_list": page_list,
                                                      "price_filter": price_filter,
                                                      "categories": categories,
                                                      "product": product_list,
                                                      "maximum_price": maximum_price,
                                                      "half_max_price": half_max_price,
                                                      "notification_count": notification_count,
                                                      "notification": notification,
                                                      "get_cart_items": total_cart_items(request)
                                                      })
    context = {
        "products": product_list,
        "price_filter": price_filter,
        "maximum_price": maximum_price,
        "half_max_price": half_max_price,
        "categories": categories,
        "notification_count": notification_count,
        "notification": notification,
        "page_list": page_list,
        "get_cart_items": total_cart_items(request)
    }
    return render(request, "market/market.html", context)


@login_required
@api_view(["GET", "POST"])
def high_low_price_products(request):
    query = request.GET.get('high_low_price', None)
    instance = Product.objects.all().order_by(f"{query}")[:5]
    data = ProductSerializer(instance, many=True).data

    return Response(data)


@login_required
@api_view(["GET", "POST"])
def recent_products(request):
    query = request.GET.get('recent', None)
    instance = Product.objects.all().order_by(f"{query}")[:5]
    data = ProductSerializer(instance, many=True).data

    return Response(data)


@login_required
@api_view(["GET", "POST"])
def paginate_products(request):
    page = request.GET.get('page', None)

    starting_number = (int(page) - 1) * 5
    ending_number = int(page) * 5

    instance = Product.objects.all().order_by("-product_purchase")[starting_number:ending_number]
    print(instance)
    data = ProductSerializer(instance, many=True).data

    return Response(data)


@login_required
def product_detail(request, pk):
    notification = Notification.objects.filter(user=request.user, is_seen=False).order_by("-id")[:10]
    notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()
    obj = get_object_or_404(Product, pk=pk)
    seller_products = Product.objects.filter(vendor=obj.vendor).exclude(name=obj).order_by("?")[:4]
    if request.method == 'POST':
        if obj.vendor.user == request.user:
            for i in obj.productimage_set.all():
                image_path = i.image.path
                if os.path.exists(image_path):
                    os.remove(image_path)
            obj.delete()
        messages.success(request, f'{obj} HAS BEEN SUCCESSFULLY DELETED!')
        return redirect(f'/vendor/{obj.vendor}/')

    ratings = [i.rating for i in obj.productreview_set.all()]
    if len(ratings) < 1:
        overall_rating = 0
        one_star = 0
        two_star = 0
        three_star = 0
        four_star = 0
        five_star = 0
    else:
        overall_rating = mean(ratings)
        one_star = float(ratings.count(1) * 100) / len(ratings)
        two_star = float(ratings.count(2) * 100) / len(ratings)
        three_star = float(ratings.count(3) * 100) / len(ratings)
        four_star = float(ratings.count(4) * 100) / len(ratings)
        five_star = float(ratings.count(5) * 100) / len(ratings)

    context = {
        "product": obj,
        "overall_rating": str(overall_rating)[:3],
        "notification_count": notification_count,
        "notification": notification,
        # "product_image": image,
        "form": ReviewBox(),
        "seller_products": seller_products,
        "get_cart_items": total_cart_items(request),

        "one_star": str(one_star)[:5],
        "two_star": str(two_star)[:5],
        "three_star": str(three_star)[:5],
        "four_star": str(four_star)[:5],
        "five_star": str(five_star)[:5],
    }
    return render(request, "market/product_detail.html", context)


@login_required
def checkout(request):
    notification = Notification.objects.filter(user=request.user, is_seen=False).order_by("-id")[:10]
    notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()
    check_out_list = Checkout.objects.filter(user=request.user, complete=False).order_by("-id")
    get_cart_total = sum([(item.product.price * item.quantity) for item in check_out_list])
    context = {
        "notification_count": notification_count,
        "notification": notification,
        "items": check_out_list,
        "get_cart_total": get_cart_total,
        "get_cart_items": total_cart_items(request),
        "paystack_public_key": settings.PAYSTACK_PUBLIC_KEY
    }
    return render(request, "market/checkout.html", context)


@login_required
def create_view(request):
    if Vendor.objects.filter(user=request.user).exists():
        notification = Notification.objects.filter(user=request.user, is_seen=False).order_by("-id")[:10]
        notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()
        product = Product.objects.last()
        if request.method == "POST":
            form = ProductForm(request.POST, request.FILES)
            education_field = CategoryField(request.POST)
            imageset = ImageField(request.POST, request.FILES)
            images = request.FILES.getlist('images')
            if form.is_valid():
                form = form.save(commit=False)
                form.vendor = request.user.vendor
                form.save()
                for image in images:
                    ProductImage.objects.create(image=image, product=form)
                    # images.save()
                for user_noti in request.user.post_notification.all():
                    notify = Notification(product=form, sender=form.vendor.user, user=user_noti, notification_type=3)
                    notify.save()
                messages.success(request, 'Your product has been created.')
                return redirect(f'/vendor/{request.user.vendor}/')
        else:
            form = ProductForm()
            education_field = CategoryField()
            imageset = ImageField()
        context = {
            "notification_count": notification_count,
            "product": product,
            "notification": notification,
            "form": form,
            "education_field": education_field,
            "imageset": imageset,
            "get_cart_items": total_cart_items(request)
        }
        return render(request, "market/create.html", context)
    else:
        return redirect("create_store")


# @login_required
def search(request):
    if request.user.is_authenticated:
        notification = Notification.objects.filter(user=request.user, is_seen=False).order_by("-id")[:10]
        notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()
        if request.method == "GET":
            query = request.GET.get('q')
            submitbutton = request.GET.get('submit')
            if query is not None:
                lookups_user = Q(user__username__icontains=query)
                lookups_product = Q(name__icontains=query)
                result_user = Vendor.objects.filter(lookups_user).distinct()
                # result_user = User.objects.filter(lookups_user).distinct()
                result_product = Product.objects.filter(lookups_product).distinct()
                context = {
                    'submitbutton': submitbutton,
                    "result_user": result_user,
                    "result_product": result_product,
                    "notification_count": notification_count,
                    "notification": notification,
                    "get_cart_items": total_cart_items(request)
                }
                return render(request, "market/search.html", context)
            else:
                context = {
                    'submitbutton': submitbutton,
                    "notification_count": notification_count,
                    "notification": notification,
                    "get_cart_items": total_cart_items(request)
                }
                return render(request, 'market/search.html', context)
        return render(request, "market/search.html", {})
    else:
        if request.method == "GET":
            query = request.GET.get('q')
            submitbutton = request.GET.get('submit')
            if query is not None:
                lookups_user = Q(user__username__icontains=query)
                lookups_product = Q(name__icontains=query)
                result_user = Vendor.objects.filter(lookups_user).distinct()
                result_product = Product.objects.filter(lookups_product).distinct()
                # combined_search = sorted(
                #     chain(result_user, result_product),
                #     key=lambda posts: posts
                # )
                context = {
                    'submitbutton': submitbutton,
                    "result_user": result_user,
                    "result_product": result_product,
                    "get_cart_items": 0

                }
                return render(request, "market/search.html", context)
            else:
                return render(request, 'market/search.html', )
        context = {

        }
        return render(request, "market/search.html", context)


class ProductInline(object):
    form_class = ProductForm
    model = Product
    template_name = "market/update_product.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        messages.success(self.request, f"{form.instance.name} HAS BEEN SUCCESSFULLY UPDATED")

        return redirect(form.instance.get_absolute_url())

    def formset_images_valid(self, formset):
        """
        Hook for custom formset saving. Useful if you have multiple formsets
        """
        images = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for image in images:
            image.product = self.object
            image.save()


class ProductUpdate(LoginRequiredMixin, UserPassesTestMixin, ProductInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(ProductUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        ctx['get_cart_items'] = total_cart_items(self.request)
        ctx["notification"] = Notification.objects.filter(user=self.request.user, is_seen=False).order_by("-id")[:10]
        ctx["notification_count"] = Notification.objects.filter(user=self.request.user, is_seen=False).count()
        ctx["category_field"] = CategoryField(instance=self.object)

        return ctx

    def get_named_formsets(self):
        return {
            'images': ImageFormSet(self.request.POST or None, self.request.FILES or None,
                                   instance=self.object, prefix='images'),
        }

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.vendor.user:
            return True
        return False


@login_required
def add_to_checkout(request, pk):
    user = request.user
    product = get_object_or_404(Product, pk=pk)
    checkout_list = Checkout.objects.filter(user=user, complete=False)
    if checkout_list.exists():
        latest_vendor = Checkout.objects.filter(user=user, complete=False).last()
        if str(product.vendor.user) == str(latest_vendor.product.vendor.user):
            create_object, created = Checkout.objects.get_or_create(
                user=user,
                product=product,
                complete=False,
            )
            create_object.quantity = (create_object.quantity + 1)
            create_object.price = (create_object.quantity * create_object.product.price)
            create_object.save()
            if create_object.quantity > 1:
                messages.success(request, f'"{product}" quantity has been updated!')
            else:
                messages.success(request, f'"{product}" has been added to your cart!')
            return redirect("checkout")

        else:
            messages.error(request, "You can't shop on a different store without checkout!😔😒")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        create_object, created = Checkout.objects.get_or_create(
            user=user,
            product=product,
            complete=False,
        )
        create_object.quantity = (create_object.quantity + 1)
        create_object.price = (create_object.quantity * create_object.product.price)
        create_object.save()
        if create_object.quantity > 1:
            messages.success(request, f'"{product}" quantity has been updated!')
        else:
            messages.success(request, f'"{product}" has been added to your cart!')
        return redirect("checkout")


@login_required
def remove_from_checkout(request, pk):
    customer = request.user
    product = get_object_or_404(Product, pk=pk)
    orderItem, created = Checkout.objects.get_or_create(user=customer, product=product, complete=False)
    if Checkout.objects.filter(user=customer, product=product).exists():
        if orderItem.quantity <= 0:
            orderItem.delete()
            messages.success(request, f"'{product.name}' has been removed from your cart/checkout")
            return redirect("checkout")
        if orderItem.quantity >= 1:
            orderItem.quantity = (orderItem.quantity - 1)
            orderItem.price = (orderItem.quantity * orderItem.product.price)
            orderItem.save()
            messages.success(request, f"'{product.name}' quantity has been reduced from your cart/checkout")
            return redirect("checkout")
    else:
        messages.success(request, f"'{product.name}' has been removed from your cart/checkout")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    return render(request, 'market/checkout.html', {})


@login_required
def delete_from_checkout(request, pk):
    customer = request.user
    product = get_object_or_404(Product, pk=pk)
    print(Checkout.objects.filter(user=customer, product=product, complete=False))
    orderItem, created = Checkout.objects.get_or_create(user=customer, product=product, complete=False)
    if Checkout.objects.filter(user=customer, product=product, complete=False).exists():
        print(Checkout.objects.filter(user=customer, product=product, complete=False))
        orderItem.delete()
        messages.success(request, f"'{product.name}' has been removed from your cart")
        return redirect("checkout")
    else:
        messages.success(request, f"'{product.name}' doesn't exists in your cart")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
@checkout_middleware
def process_order(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()
    reference = str(data['ref']['reference'])
    check_out_list = Checkout.objects.filter(user=request.user, complete=False).order_by("-id")
    receiver = []
    notify_user = []
    for i in Checkout.objects.filter(user=request.user, complete=False):
        receiver.append(i.product.vendor)
        notify_user.append(i.product.vendor.user)

    queryset = []
    for item in check_out_list:
        queryset.append(item.complete == True)
        item.complete = True
        item.save()

    vendor_current_balance = sum([item.get_total for item in check_out_list])
    receiver[0].current_balance += vendor_current_balance
    receiver[0].total_earnings += vendor_current_balance
    receiver[0].save()

    order = Order.objects.create(
        user=request.user,
        transaction_id=transaction_id,
        ordered=True,
        vendor=receiver[0]
    )
    order.order_item.set([item for item in check_out_list])
    order.default_order_item = [str(item) for item in order.order_item.all()]
    order.default_price = sum([item.get_total for item in check_out_list])
    order.save()
    product_queryset = []
    for item in check_out_list:
        product_queryset.append(item.product.product_purchase + item.quantity)
        item.product.product_purchase += item.quantity
        item.product.save()

    notification = Notification.objects.create(
        user=notify_user[0],
        sender=request.user,
        notification_type=1
    )
    notification.orders.set([item for item in check_out_list])
    notification.save()
    Payment.objects.create(
        amount=order.total_order_item_price,
        ref=reference,
        email=request.user.email,
        verified=True
    )
    # Work on the payment option!
    # payment = get_object_or_404(Payment, ref=ref)
    # verified = payment.verified()
    # if verified:
    #     messages.success(request, "Verification passed!")
    # else:
    #     messages.error(request, "Verification failed")
    return JsonResponse('Payment complete!', safe=False)


@login_required
def product_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ReviewBox(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.customer_info = request.user
            form.product = product
            form.default_product = str(product)
            form.save()

            ratings = [i.rating for i in product.productreview_set.all()]
            product.rating_count = round(mean(ratings))
            product.save()

    data = {
        "comment": request.POST.get('comment', None),
        "message": "Your review has been sent"
    }

    return JsonResponse(data)


def error_404(request, exception):
    data = {}
    return render(request, 'market/error404.html', data)


def error_500(request):
    data = {}
    return render(request, 'market/error404.html', data)


