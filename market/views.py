from abc import ABC

from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, Vendor, ProductImage, Checkout, ProductReview
from django.db.models import Q
from users.models import User, Notification
from itertools import chain
from .forms import CreateProductForm, CategoryField, ImageField, ReviewBox
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, serializers
from django.views.generic import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.paginator import Paginator


# Create your views here.
def total_cart_items(request):
    check_out_list = Checkout.objects.filter(user=request.user)
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
    notification = Notification.objects.filter(user=request.user, is_seen=False).order_by("-id")[:3]
    notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()
    categories = Category.objects.all()
    product_list = Product.objects.all()

    products = Paginator(product_list, 4)
    first_page = products.page(1).object_list
    page_range = products.page_range
    # page_number = request.GET.get('page')
    # products = paginator.get_page(page_number)

    if request.method == 'POST':
        # getting page number
        page_no = request.POST.get('page_no', None)
        results = list(products.page(page_no).object_list.values('name', 'price', 'image',
                                                                 "product_purchase", "vendor__username", "vendor__image", "pk"))
        return JsonResponse({"results": results})
    # else:
    #     return render(request, 'market/search.html', )

    if request.GET.get('category_id'):
        filterProduct = Product.getProductByFilter(request.GET['category_id']).order_by('-id')
        filter_category_product = filterProduct.all().order_by('-id')

        return render(request, 'market/market.html', {"products": filter_category_product,
                                                      "categories": categories,
                                                      'product': products,
                                                      "notification_count": notification_count,
                                                      "notification": notification,
                                                      "get_cart_items": total_cart_items(request)
                                                      })
    context = {
        # "products": first_page,
        "products": product_list,
        "page_range": page_range,
        "categories": categories,
        "notification_count": notification_count,
        "notification": notification,
        "get_cart_items": total_cart_items(request)
    }
    return render(request, "market/market.html", context)


@login_required
def product_detail(request, pk):
    notification = Notification.objects.filter(user=request.user, is_seen=False).order_by("-id")[:3]
    notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()
    obj = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        if obj.vendor == request.user:
            obj.delete()
        messages.success(request, f'{obj} HAS BEEN SUCCESSFULLY DELETED!')
        return redirect(f'/{obj.vendor}/vendor/')

    image = []
    for image in obj.productimage_set.all():
        image

    context = {
        "product": obj,
        "notification_count": notification_count,
        "notification": notification,
        "product_image": image,
        "form": ReviewBox(),
        "get_cart_items": total_cart_items(request)
    }
    return render(request, "market/product_detail.html", context)


@login_required
def checkout(request):
    notification = Notification.objects.filter(user=request.user, is_seen=False).order_by("-id")[:3]
    notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()
    check_out_list = Checkout.objects.filter(user=request.user)
    get_cart_total = sum([(item.product.price * item.quantity) for item in check_out_list])
    get_cart_items = sum([item.quantity for item in check_out_list])

    context = {
        "notification_count": notification_count,
        "notification": notification,
        "items": check_out_list,
        "get_cart_total": get_cart_total,
        "get_cart_items": total_cart_items(request)
    }
    return render(request, "market/checkout.html", context)


@login_required
def create_view(request):
    if Vendor.objects.filter(user=request.user).exists():
        notification = Notification.objects.filter(user=request.user, is_seen=False).order_by("-id")[:3]
        notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()
        product = Product.objects.last()
        if request.method == "POST":
            form = CreateProductForm(request.POST, request.FILES)
            education_field = CategoryField(request.POST)
            imageset = ImageField(request.POST, request.FILES)
            images = request.FILES.getlist('images')
            if form.is_valid():
                form = form.save(commit=False)
                form.vendor = request.user
                form.save()
                print(images)
                for image in images:
                    ProductImage.objects.create(image=image, product=form)
                    # images.save()
                for user_noti in request.user.post_notification.all():
                    notify = Notification(product=form, sender=form.vendor, user=user_noti, notification_type=3)
                    notify.save()
                messages.warning(request, 'Your product has been created.')
                return redirect(f'/{request.user.vendor}/vendor/')
        else:
            form = CreateProductForm()
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
        notification = Notification.objects.filter(user=request.user, is_seen=False).order_by("-id")[:3]
        notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()
        if request.method == "GET":
            query = request.GET.get('q')
            submitbutton = request.GET.get('submit')
            if query is not None:
                lookups_user = Q(username__icontains=query)
                lookups_product = Q(name__icontains=query)
                result_user = User.objects.filter(lookups_user).distinct()
                result_product = Product.objects.filter(lookups_product).distinct()
                # combined_search = sorted(
                #     chain(result_user, result_product),
                #     key=lambda posts: posts
                # )
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
                return render(request, 'market/search.html', )
        context = {

        }
        return render(request, "market/search.html", context)
    else:
        if request.method == "GET":
            query = request.GET.get('q')
            submitbutton = request.GET.get('submit')
            if query is not None:
                lookups_user = Q(username__icontains=query)
                lookups_product = Q(name__icontains=query)
                result_user = User.objects.filter(lookups_user).distinct()
                result_product = Product.objects.filter(lookups_product).distinct()
                # combined_search = sorted(
                #     chain(result_user, result_product),
                #     key=lambda posts: posts
                # )
                context = {
                    'submitbutton': submitbutton,
                    "result_user": result_user,
                    "result_product": result_product,
                    "get_cart_items": total_cart_items(request)

                }
                return render(request, "market/search.html", context)
            else:
                return render(request, 'market/search.html', )
        context = {

        }
        return render(request, "market/search.html", context)


class UserFollowerApi(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username, format=None):
        obj = get_object_or_404(User, username=username)
        user = request.user
        updated = False
        following = False

        if user in obj.follower.all():
            following = False
            obj.follower.remove(user)
            user.following.remove(obj)
            obj.post_notification.remove(user)

            notify = Notification.objects.get(sender=user, user=obj, notification_type=2)
            notify.delete()

        else:
            following = True
            obj.follower.add(user)
            user.following.add(obj)

            notify = Notification(sender=user, user=obj, notification_type=2)
            notify.save()

            data = {
                'updated': updated,
                'following': following,
                'follower_count': obj.follower.count(),
            }
            return Response(data)
        updated = True

        data = {
            'updated': updated,
            'following': following,
            'follower_count': obj.follower.count(),
        }
        return Response(data)


class PostNotificationApi(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username, format=None):
        user = request.user
        obj = get_object_or_404(User, username=username)
        updated = False
        post_notify = False
        if user:
            if user in obj.post_notification.all():
                post_notify = False
                obj.post_notification.remove(user)
            else:
                post_notify = True
                obj.post_notification.add(user)

                data = {
                    "updated": updated,
                    "post_notify": post_notify,
                    "messages": "You will get notified when they post"
                }
                return Response(data)
            updated = True
        data = {
            "updated": updated,
            "post_notify": post_notify,
            "messages": "You will get notified when they post"
        }
        return Response(data)


class UpdateProductView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, ABC):
    model = Product
    fields = ['category', 'name', 'price', 'description',]

    def form_valid(self, form):
        form.instance.vendor = self.request.user
        messages.success(self.request, f"{form.instance.name} HAS BEEN SUCCESSFULLY UPDATED")
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.vendor:
            return True
        return False


@login_required
def update_product(request, pk):
    obj = get_object_or_404(Product, pk=pk)
    notification = Notification.objects.filter(user=request.user, is_seen=False).order_by("-id")[:3]
    notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()
    if request.user == obj.vendor:
        if request.method == "POST":
            form = CreateProductForm(request.POST, request.FILES, instance=obj)
            category_field = CategoryField(request.POST, instance=obj)
            imageset = ImageField(request.POST, request.FILES, instance=obj)
            images = request.FILES.getlist('images')
            if form.is_valid() and imageset.is_valid():
                form = form.save(commit=False)
                form.vendor = request.user
                form.save()
                print(images)
                for image in imageset.cleaned_data:
                    f = image['images']
                    print(f)
                    if ProductImage.objects.filter(product=form, image=image).exists():
                        ProductImage.objects.filter(product=form, image=image).update(image=image)
                    else:
                        ProductImage.objects.create(image=image, product=form)

                # if ProductImage.objects.filter(product=form).exists():
                #     for image in images:
                #         ProductImage.objects.filter(product=form, image=image).update(image=image)
                # else:
                #     for image in images:
                #         ProductImage.objects.create(image=image, product=form)
                # images.save()
                for user_noti in request.user.post_notification.all():
                    notify = Notification(product=form, sender=form.vendor, user=user_noti, notification_type=3)
                    notify.save()
                messages.success(request, 'Your product has been updated.')
                return redirect(f'/product/{obj.id}/')
        else:
            form = CreateProductForm(instance=obj)
            category_field = CategoryField(instance=obj)
            imageset = ImageField(instance=obj)
            print(imageset)
        context = {
            "notification_count": notification_count,
            "product": obj,
            "notification": notification,
            "form": form,
            "category_field": category_field,
            "imageset": imageset
        }
        return render(request, "market/update_product.html", context)
    else:
        messages.error(request, "You are not allowed!")
        return redirect("error404")


@login_required
def add_to_checkout(request, pk):
    user = request.user
    product = get_object_or_404(Product, pk=pk)
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
    orderItem, created = Checkout.objects.get_or_create(user=customer, product=product)
    if Checkout.objects.filter(user=customer, product=product).exists():
        if orderItem.quantity <= 0:
            orderItem.delete()
            messages.success(request, f"'{product.name}' has been removed from your cart")
            return redirect("checkout")
        if orderItem.quantity >= 1:
            orderItem.quantity = (orderItem.quantity - 1)
            orderItem.price = (orderItem.quantity * orderItem.product.price)
            orderItem.save()
            return redirect("checkout")
    else:
        messages.success(request, f"'{product.name}' has been removed from your cart")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    return render(request, 'market/checkout.html', {})


@login_required
def productReview(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ReviewBox(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.customer_info = request.user
            form.product = product
            form.save()

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
