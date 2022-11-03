from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import auth
from .forms import *
from django.contrib import messages
from .models import *
from market.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, serializers
from datetime import datetime, date
from django.core.serializers.json import DjangoJSONEncoder


# Create your views here.
def total_cart_items(request):
    check_out_list = Checkout.objects.filter(user=request.user, complete=False)
    get_cart_items = sum([item.quantity for item in check_out_list])

    return get_cart_items


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form_password = form.clean_password2()
            form = form.save(commit=False)
            email = form.email
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
                return redirect("register")
            else:
                form.save()
                auth_login = auth.authenticate(username=form.username, password=form_password)
                auth.login(request, auth_login)
                return redirect("market")
    else:
        form = UserRegisterForm()
    context = {
        "form": form
    }
    return render(request, "users/register.html", context)


@login_required
def create_store(request):
    user = request.user
    if not Vendor.objects.filter(user=request.user).exists():
        notification = Notification.objects.filter(user=request.user, is_seen=False)[:7]
        notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()
        if request.method == 'POST':
            u_form = StoreCreateForm(request.POST)
            if u_form.is_valid():
                u_form = u_form.save(commit=False)
                u_form.user = request.user
                u_form.save()
                print(u_form)
                messages.success(request, f'Your store has been created by {user}.')
                return redirect('create')
        else:
            u_form = StoreCreateForm()
        context = {
            'u_form': u_form,
            "notification_count": notification_count,
            "notification": notification,
            "get_cart_items": total_cart_items(request)
        }
        return render(request, 'users/create_store.html', context)
    else:
        messages.warning(request, 'You are already a vendor')
        return redirect(f'/{user}/vendor/')


@login_required
def vendor_view(request, username):
    try:
        notification = Notification.objects.filter(user=request.user, is_seen=False).order_by("-id")[:7]
        notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()
        vendor = get_object_or_404(User, username=username)
        products = vendor.product_set.all()
    except ObjectDoesNotExist:
        return redirect("market")
    context = {
        "vendor": vendor,
        "products": products,
        "notification_count": notification_count,
        "notification": notification,
        "get_cart_items": total_cart_items(request),
        "form": UserUpdateForm(instance=request.user)
    }
    return render(request, "users/vendor_post.html", context)


class DateExtendedEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            try:
                return o.strftime("%b %d")
            except ValueError as e:
                return ''
        else:
            return super().default(o)


def solution(date_list, time_list):
    """
    dates = ["Nov 2", "Nov 2", "Nov 4", "Nov 4", "Nov 5", "Nov 5", "Nov 7", "Nov 7", "Nov 8", "Nov 8"]
    times = [2, 3, 2, 2, 3, 3, 1, 8, 2, 3]

    final_result = {'Nov 2': 5, 'Nov 4': 4, 'Nov 5': 6, 'Nov 7': 9, 'Nov 8': 5}
    """
    checker = list(zip(date_list, time_list))
    ans = {}

    for i in list(date_list):
        summation = 0
        for j in checker:
            if j[0] == i:
                summation += j[1]
        ans[i] = summation

    nested_list = list(ans.items())  # converts ans to a nested list
    single_list = [j for i in nested_list for j in i]  # run through the list to return a single list
    it = iter(single_list[-12:])  # get last N values
    result_dict = dict(zip(it, it))  # converts it to a dictionary

    return result_dict


@login_required
def vendor_dashboard(request):
    if Vendor.objects.filter(user=request.user).exists():
        notification = Notification.objects.filter(user=request.user, is_seen=False).order_by("-id")
        notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()

        vendor = request.user
        # vendor_profile = Vendor.object.get(user=vendor)
        products = vendor.product_set.all()
        today_product = Product.objects.filter(vendor=vendor, date_posted__gte=date.today())
        orders = Checkout.objects.filter(product__vendor=vendor, complete=True).order_by('-date_posted')[:5]
        orders_earnings = Checkout.objects.filter(product__vendor=vendor, complete=True).order_by('-date_posted')
        today_order = Checkout.objects.filter(product__vendor=vendor, complete=True, date_posted__gte=date.today())
        monthly_order = Checkout.objects.filter(product__vendor=vendor,
                                                complete=True, date_posted__month__gte=datetime.now().month)
        best_selling_products = Product.objects.filter(vendor=request.user).order_by('-product_purchase')[:5]
        earnings = sum([(i.product.price * i.quantity) for i in orders_earnings])
        today_earning = sum([(i.product.price * i.quantity) for i in today_order])
        monthly_earning = sum([(i.product.price * i.quantity) for i in monthly_order])
        # print([(i.product.price * i.quantity) for i in monthly_order])
        # print([DateExtendedEncoder.default(i.date_posted, i.date_posted) for i in monthly_order])
        chart_products = Checkout.objects.filter(product__vendor=vendor, complete=True).order_by("date_posted")

        date_list = []

        for i in Checkout.objects.filter(product__vendor=vendor, complete=True).order_by("date_posted"):
            date_list.append(DateExtendedEncoder.default(i.date_posted, i.date_posted))
            # uniques = []
            # for number in date_list:
            #     if number not in uniques:
            #         uniques.append(number)

        chart_value = solution(date_list, [i.quantity for i in chart_products])
        get_values = chart_value.values()
        get_keys = chart_value.keys()
        # print(list(get_keys))
        # print(uniques)

    else:
        messages.warning(request, "You need to register as a Vendor to view dashboard.")
        return redirect("create_store")

    context = {
        "vendor": vendor,
        "products": products,
        "chart_products": get_values,
        "today_product": today_product,
        "orders": orders,
        "today_order": today_order,
        # "vendor_profile": vendor_profile,
        "DOW_CHOICES": list(get_keys),
        "best_selling_products": best_selling_products,
        "notification_count": notification_count,
        "notification": notification,
        "earnings": earnings,
        "today_earning": today_earning,
        "monthly_earning": monthly_earning,
        "get_cart_items": total_cart_items(request),
    }
    return render(request, "users/dashboard.html", context)


@login_required
def update_profile(request):
    notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form = form.save(commit=False)
            image_path = form.image.path

            # if os.path.exists(image_path):
            #     os.remove(image_path)
            #     print(image_path)

            form.save()
            print(image_path)

            messages.success(request, 'Your account has been updated!')
            return redirect(f"../{request.user}/vendor/")
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            # i changed the error popup
            messages.warning(request, 'error')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = UserUpdateForm(instance=request.user)
    context = {
        "form": form,
        "notification_count": notification_count,
    }
    return render(request, 'users/update_profile.html', context)


@login_required
def notification_view(request):
    followed_by = request.user.following.filter(id__in=request.user.follower.all())[:1]
    followed_by_ = request.user.following.filter(id__in=request.user.follower.all())
    followed_by_count = followed_by_.count()
    notification = Notification.objects.filter(user=request.user, is_seen=False).order_by("-date_posted")[:7]
    post_notification = Notification.objects.filter(user=request.user, is_seen=False)

    if not notification:
        notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()
        notification_list = Notification.objects.filter(user=request.user).order_by("-date_posted")

        context = {
            "notification_list": notification_list,
            "notification_count": notification_count,
            "notification": notification,
            "followed_by": followed_by,
            "followed_by_count": followed_by_count,
            "get_cart_items": total_cart_items(request)

        }
        return render(request, "users/notification.html", context)
    elif not post_notification:
        notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()
        notification_list = Notification.objects.filter(user=request.user).order_by("-date")

        queryset = []
        for let in notification_list:
            queryset.append(let.blog)
        context = {
            "notification_list": notification_list,
            "notification_count": notification_count,
            "followed_by": followed_by,
            "followed_by_count": followed_by_count,
            "get_cart_items": total_cart_items(request)

            # "queryset": queryset
        }
        return render(request, "users/notification.html", context)
    else:
        notification_list = Notification.objects.filter(user=request.user).order_by("-date_posted").exclude(
            notification_type=7)
        notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()

        queryset = []
        for let in Notification.objects.filter(user=request.user):
            queryset.append(let.is_seen == True)
            let.is_seen = True
            let.save()

        context = {
            "notification_list": notification_list,
            "notification": notification,
            "notification_count": notification_count,
            "followed_by": followed_by,
            "followed_by_count": followed_by_count,
            "get_cart_items": total_cart_items(request)

        }
        return render(request, "users/notification.html", context)


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
