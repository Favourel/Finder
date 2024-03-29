from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, Http404
from django.contrib.auth.models import auth
from .forms import *
from django.conf import settings as setting

from django.contrib import messages
from .models import *
from market.models import *
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import authentication, permissions, serializers
from datetime import datetime, date, timedelta
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from market.serializers import OrderSerializer
from django.db.models import F
from django.http import HttpResponse
import csv
from django.contrib.humanize.templatetags.humanize import intcomma


# Create your views here.
def total_cart_items(request):
    check_out_list = Checkout.objects.filter(user=request.user, complete=False)
    get_cart_items = sum([item.quantity for item in check_out_list])

    return get_cart_items


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        registration_method = request.POST.get('registration_method')
        if password1 == password2:
            if User.objects.filter(username__iexact=username).exists():
                messages.error(request, 'A user with that username already exists.')
                return redirect('register')
            elif User.objects.filter(email__iexact=email).exists():
                messages.error(request, 'A user with that email address already exists.')
                return redirect('register')
            elif len(password1) < 8 and len(password2) < 8:
                messages.error(request, 'Password can not be less than 8')
                return redirect('register')
            elif password1 and password2 == username:
                messages.error(request, 'Password can not similar to username')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                auth_login = auth.authenticate(username=username, password=password1)
                auth.login(request, auth_login)
                if registration_method == "client":
                    messages.success(request, f"Account has been successfully created for {username}")
                    return redirect('market')
                elif registration_method == "vendor":
                    messages.success(request, f"Account has been successfully created for {username}")
                    return redirect('create_store')
        else:
            messages.error(request, "The two password fields didn’t match.")
            return redirect('register')
    context = {

    }
    return render(request, 'users/register.html', context)


def validate_username(request):
    username = request.GET.get('username', None)
    email = request.GET.get('email', None)
    password1 = request.GET.get('password1', None)
    password2 = request.GET.get('password2', None)
    updated = False

    if password1 != password2:
        not_match = "The two password fields didn’t match."
        data = {
            'is_taken': User.objects.filter(username__iexact=username).exists(),
            'is_taken_email': User.objects.filter(email__iexact=email).exists(),
            "not_match": not_match,
            "updated": updated,
        }
        return JsonResponse(data)

    elif password1 and password2 is not None:
        if len(password1) < 8 and len(password2) < 8:
            lt_password = "Passwords can not be less than 8"
            data = {
                # 'is_taken': User.objects.filter(username__iexact=username).exists(),
                # 'is_taken_email': User.objects.filter(email__iexact=email).exists(),
                "updated": updated,
                "lt_password": lt_password,
            }
            return JsonResponse(data)

    updated = True

    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists(),
        'is_taken_email': User.objects.filter(email__iexact=email).exists(),
        "updated": updated
    }
    return JsonResponse(data)


@login_required
def create_store(request):
    user = request.user
    if not Vendor.objects.filter(user=request.user).exists():
        notification = Notification.objects.filter(user=request.user, is_seen=False)[:7]
        notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()
        if request.method == 'POST':
            u_form = StoreCreateForm(request.POST, request.FILES)
            if u_form.is_valid():
                u_form = u_form.save(commit=False)
                u_form.user = request.user
                u_form.save()
                loggedin_user = User.objects.get(username=user.username)
                loggedin_user.phone_number = u_form.phone_number
                loggedin_user.location = u_form.location
                loggedin_user.image = u_form.image
                loggedin_user.save()
                notification = Notification.objects.create(
                    user=user,
                    sender=User.objects.first(),
                    notification_type=4,
                )
                notification.save()
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
        return redirect(f'/vendor/{user}/')


@login_required
def vendor_view(request, username):
    try:
        notification = Notification.objects.filter(user=request.user, is_seen=False).order_by("-id")[:10]
        notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()
        vendor = get_object_or_404(Vendor, user__username=username)
        products = vendor.product_set.all()
        Vendor.objects.filter(user__username=username).update(account_visit=F("account_visit") + 1)
    except Http404:
        messages.error(request, "The searched word has no active store/profile")
        return redirect("error404")
    context = {
        "vendor": vendor,
        "products": products,
        "notification_count": notification_count,
        "notification": notification,
        "get_cart_items": total_cart_items(request),
        "form": StoreCreateForm(instance=vendor)
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
    it = iter(single_list[-14:])  # get last N values
    result_dict = dict(zip(it, it))  # converts it to a dictionary

    return result_dict


@login_required
def vendor_dashboard(request):
    if Vendor.objects.filter(user=request.user).exists():
        notification = Notification.objects.filter(user=request.user, is_seen=False).order_by("-id")[:10]
        notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()

        vendor = request.user.vendor
        products = Product.objects.filter(vendor=vendor)
        today_product = Product.objects.filter(vendor=vendor, date_posted__gte=date.today())
        best_selling_products = Product.objects.filter(vendor=vendor).order_by('-product_purchase')[:5]
        product_purchase = Product.objects.filter(vendor=vendor).last()

        orders = Order.objects.filter(vendor=vendor, ordered=True).order_by("-date_posted")[:4]
        today_order = Order.objects.filter(vendor=vendor, date_posted__gte=date.today())
        monthly_order = Order.objects.filter(vendor=vendor, ordered=True,
                                             date_posted__gte=datetime.now() - timedelta(days=30))
        past_monthly_order = Order.objects.filter(vendor=vendor, ordered=True,
                                                  date_posted__gte=datetime.now() - timedelta(days=30))
        # past_monthly_order = Order.objects.filter(vendor=vendor, ordered=True,
        #                                           date_posted__month__lt=datetime.now().month)
        weekly_order = Order.objects.filter(vendor=vendor, ordered=True,
                                            date_posted__gte=datetime.now() - timedelta(days=7))
        yesterday_order = Order.objects.filter(vendor=vendor, ordered=True,
                                               date_posted__date=datetime.now().date() - timedelta(days=1))
        all_order = Order.objects.filter(vendor=vendor, ordered=True).order_by("-date_posted")

        current = len(all_order)
        previous = current - len(weekly_order)
        if current & previous > 0:
            percentage_order = ((current - previous) / previous) * 100
        else:
            percentage_order = 0

        # current_yesterday = current - len(yesterday_order)
        # if current & len(yesterday_order) > 0:
        #     percentage_order_yesterday = ((current_yesterday - len(yesterday_order)) / len(yesterday_order)) * 100
        # else:
        #     percentage_order_yesterday = 0
        if current & len(yesterday_order) > 0:
            percentage_order_yesterday = ((len(today_order) - len(yesterday_order)) / len(yesterday_order)) * 100
        else:
            percentage_order_yesterday = 0

        current_monthly = current - len(past_monthly_order)

        if current & len(past_monthly_order) > 0:
            percentage_order_monthly = ((current_monthly - len(past_monthly_order)) / len(past_monthly_order)) * 100
        else:
            percentage_order_monthly = 0

        iter_customers = [i.user for i in all_order]
        uniques = []
        for number in iter_customers:
            if number not in uniques:
                uniques.append(number)

        iter_customers_today = [i.user for i in today_order]
        uniques_customers_today = []
        for number in iter_customers_today:
            if number not in uniques_customers_today:
                uniques_customers_today.append(number)

        iter_customers_weekly = [i.user for i in weekly_order]
        uniques_customers_weekly = []
        for number in iter_customers_weekly:
            if number not in uniques_customers_weekly:
                uniques_customers_weekly.append(number)

        iter_customers_monthly = [i.user for i in monthly_order]
        uniques_customers_monthly = []
        for number in iter_customers_monthly:
            if number not in uniques_customers_monthly:
                uniques_customers_monthly.append(number)

        current = len(uniques)
        previous = current - len(uniques_customers_weekly)

        if current & previous > 0:
            percentage_customers = ((current - previous) / previous) * 100
        else:
            percentage_customers = 0

        earnings = sum([i.default_price for i in all_order])
        today_earning = sum([i.default_price for i in today_order])
        yesterday_earning = sum([i.default_price for i in yesterday_order])
        past_monthly_earning = sum([i.default_price for i in past_monthly_order])
        monthly_earning = sum([i.default_price for i in monthly_order])
        weekly_earning = sum([i.default_price for i in weekly_order])

        current = int(earnings)
        previous = current - int(weekly_earning)

        if current & previous > 0:
            percentage_earnings = ((current - previous) / previous) * 100
        else:
            percentage_earnings = 0

        previous_yesterday = current - int(yesterday_earning)
        if current & previous_yesterday > 0:
            percentage_earning_yesterday = ((current - previous_yesterday) / previous_yesterday) * 100
        else:
            percentage_earning_yesterday = 0

        current_monthly = current - int(past_monthly_earning)

        if current & int(past_monthly_earning) > 0:
            percentage_earning_monthly = ((current_monthly - int(past_monthly_earning)) / int(past_monthly_earning)) * 100
        else:
            percentage_earning_monthly = 0

        chart_products = Order.objects.filter(vendor=vendor, ordered=True).order_by("date_posted")

        date_list = []

        for i in Order.objects.filter(order_item__product__vendor=vendor, ordered=True).order_by("date_posted"):
            date_list.append(DateExtendedEncoder.default(i.date_posted, i.date_posted))
            # uniques = []
            # for number in date_list:
            #     if number not in uniques:
            #         uniques.append(number)

        chart_value = solution(date_list, [j.quantity for i in chart_products for j in i.order_item.all()])
        get_values = chart_value.values()
        get_keys = chart_value.keys()

    else:
        messages.warning(request, "You need to register as a Vendor to view dashboard.")
        return redirect("create_store")
    context = {
        "notification_count": notification_count,
        "notification": notification,

        "vendor": vendor,
        "products": products,
        "today_product": today_product,

        "orders": orders,
        "all_order": all_order,
        "today_order": today_order,
        "monthly_order": monthly_order,
        "percentage_order": str(percentage_order)[:4],
        "percentage_order_yesterday": str(percentage_order_yesterday)[:4],
        "percentage_order_monthly": str(percentage_order_monthly)[:4],

        "chart_products": get_values,
        "DOW_CHOICES": list(get_keys),
        "product_purchase": product_purchase,
        "best_selling_products": best_selling_products,

        "earnings": earnings,
        "today_earning": today_earning,
        "monthly_earning": monthly_earning,
        "percentage_earning_yesterday": str(percentage_earning_yesterday)[:4],
        "percentage_earnings": str(percentage_earnings)[:4],
        "percentage_earning_monthly": str(percentage_earning_monthly)[:5],

        "get_cart_items": total_cart_items(request),
        "now": datetime.now().hour,
        "form": StoreCreateForm(instance=vendor),
        "customers": len(uniques),
        "customers_today": len(uniques_customers_today),
        "customers_monthly": len(uniques_customers_monthly),
        "percentage_customers": str(percentage_customers)[:4],

        "paystack_public_key": setting.PAYSTACK_PUBLIC_KEY,

        "account_visit": vendor.account_visit,
    }
    return render(request, "users/dashboard.html", context)


@login_required
def update_profile(request):
    notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()

    if request.method == 'POST':
        form = StoreCreateForm(request.POST, request.FILES, instance=request.user.vendor)

        if form.is_valid():
            form = form.save(commit=False)
            # image_path = form.image.path

            # if os.path.exists(image_path):
            #     os.remove(image_path)
            #     print(image_path)

            form.save()
            # print(image_path)

            messages.success(request, 'Your account has been updated!')
            # return redirect(f"../{request.user.vendor}/vendor/")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            # i changed the error popup
            messages.warning(request, 'error')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # else:
    #     form = StoreCreateForm(instance=request.user.vendor)
    # context = {
    #     "form": form,
    #     "notification_count": notification_count,
    # }
    # return render(request, 'users/update_profile.html', context)


@login_required
def notification_view(request):
    notification = Notification.objects.filter(user=request.user, is_seen=False).order_by("-date_posted")[:10]

    vendor = request.user.vendor
    post_notification = Notification.objects.filter(user=request.user, is_seen=False).order_by("-date_posted")

    if not post_notification:
        notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()
        notification_list = Notification.objects.filter(user=request.user, is_seen=True).order_by("-date_posted")

        context = {
            "notification_list": notification_list,
            "notification_count": notification_count,
            "notification": notification,
            "vendor": vendor,
            "form": StoreCreateForm(instance=vendor),
            "get_cart_items": total_cart_items(request)

        }
        return render(request, "users/notification.html", context)
    else:
        notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()

        queryset = []
        for let in Notification.objects.filter(user=request.user):
            queryset.append(let.is_seen == True)
            let.is_seen = True
            let.save()

        notification_list = Notification.objects.filter(user=request.user, is_seen=True).order_by("-date_posted")

        context = {
            "notification_count": notification_count,
            "notification_list": notification_list,
            "notification": notification,
            "vendor": vendor,
            "form": StoreCreateForm(instance=vendor),
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


@login_required
def mark_as_read(request):
    updated = False
    queryset = []
    for i in Notification.objects.filter(user=request.user):
        queryset.append(i.is_seen == True)
        i.is_seen = True
        i.save()
        updated = True
    notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()

    data = {
        "updated": updated,
        "notification_count": notification_count,
        "messages": "Notifications has been marked as read"
    }
    return JsonResponse(data)


@login_required
def settings(request):
    notification = Notification.objects.filter(user=request.user, is_seen=False).order_by("-id")[:10]
    notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()

    user = request.user
    all_order = Order.objects.filter(user=user, ordered=True).order_by("-date_posted")
    all_order_count = len(all_order)
    reviews = ProductReview.objects.filter(customer_info=user).order_by("-date_added")
    reviews_count = len(reviews)

    last_order = Order.objects.filter(user=user, ordered=True).order_by("-date_posted")[:1]
    total_spent = sum([j.get_total for i in all_order for j in i.order_item.all()])

    paginator = Paginator(all_order, 7)
    page = request.GET.get('page', 1)

    try:
        all_order = paginator.page(page)
    except PageNotAnInteger:
        all_order = paginator.page(1)
    except EmptyPage:
        all_order = paginator.page(paginator.num_pages)

    page_list = all_order.paginator.page_range

    paginator = Paginator(reviews, 7)
    page_number = request.GET.get('page')
    reviews = paginator.get_page(page_number)

    if Vendor.objects.filter(user=request.user).exists():
        if request.method == "POST":
            form = StoreCreateForm(request.POST, request.FILES, instance=user.vendor)
            # email_instance = form.instance.user.email
            # print(email_instance)
            if form.is_valid():
                form = form.save(commit=False)
                form.save()
                loggedin_user = User.objects.get(username=user.username)
                loggedin_user.phone_number = form.phone_number
                loggedin_user.location = form.location
                loggedin_user.image = form.image
                loggedin_user.save()
                # email = form.email
                # if User.objects.filter(email=email).exists():
                #     if request.user.email == email_instance:
                #         form.save()
                messages.success(request, 'Your account has been updated!')
                #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                #     messages.error(request, "A user with that email already exists.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            # else:
            #     form.save()
            #     messages.success(request, 'Your account has been updated!')
            #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            form = StoreCreateForm(instance=request.user.vendor)
            # form = UserUpdateForm(instance=user)
        context = {
            "form": form,
            "get_cart_items": total_cart_items(request),
            "notification_count": notification_count,
            "notification": notification,
            "all_order": all_order,
            "all_order_count": all_order_count,
            "reviews": reviews,
            "reviews_count": reviews_count,
            "last_order": last_order,
            "total_spent": total_spent,

            "page_list": page_list,
            "list_orders": all_order,
        }
        return render(request, "users/settings.html", context)
    else:
        if request.method == "POST":
            form = UserUpdateForm(request.POST, instance=user)
            email_instance = form.instance.email
            if form.is_valid():
                form = form.save(commit=False)
                email = form.email
                if User.objects.filter(email=email).exists():
                    if request.user.email == email_instance:
                        form.save()
                        messages.success(request, 'Your account has been updated!')
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    messages.error(request, "A user with that email already exists.")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    form.save()
                    messages.success(request, 'Your account has been updated!')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            form = UserUpdateForm(instance=user)
        context = {
            "form": form,
            "get_cart_items": total_cart_items(request),
            "notification_count": notification_count,
            "notification": notification,
            "all_order": all_order,
            "all_order_count": all_order_count,
            "reviews": reviews,
            "reviews_count": reviews_count,
            "last_order": last_order,
            "total_spent": total_spent,

            "page_list": page_list,
            "list_orders": all_order,
        }
        return render(request, "users/settings.html", context)


@login_required
@api_view(["GET", "POST"])
def paginate(request):
    page = request.GET.get('page', None)
    user = request.GET.get('user', None)

    starting_number = (int(page) - 1) * 7
    ending_number = int(page) * 7

    instance = Order.objects.filter(user=user, ordered=True).order_by("-date_posted")[starting_number:ending_number]
    data = OrderSerializer(instance, many=True).data

    "By [starting_number:ending_number] we specify the interval of results. Order them by date or whatever you want"
    # data = {result}

    return Response(data)


@login_required
def delete_account(request, username):
    try:
        user_id = get_object_or_404(User, username=username)
        user_id.delete()

    except User.DoesNotExist:
        messages.error(request, "User does not exist")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except Exception as e:
        return render(request, 'users/settings.html', {'err': e.message})

    return redirect("/")


@login_required
def export_products(request):
    vendor = request.user.vendor
    queryset = Product.objects.filter(vendor=vendor)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'name', 'price', 'description',
                     'category', "product_purchase", "date_posted"])
    products = queryset.values_list('id', 'name', 'price', 'description',
                                    'category__name', "product_purchase", "date_posted")
    for product in products:
        writer.writerow(product)
    return response


@login_required
def request_withdrawal(request):
    vendor = request.user.vendor
    if request.method == "POST":
        amount = request.POST.get('amount', None)  # getting data from amount input
        password = request.POST.get('password', None)  # getting data from amount input
        if password == vendor.withdrawal_password:
            if float(amount) > 0:
                if float(amount) < float(vendor.current_balance):
                    vendor.current_balance -= float(amount)
                    vendor.save()
                    data = {
                        'msg_successfully': 'Withdrawal was successfully',  # response message
                        "current_balance": f"₦{intcomma(vendor.current_balance)}0"
                    }
                    return JsonResponse(data)
                else:
                    data = {
                        'msg_insufficient': 'Insufficient funds'  # response message
                    }
                    return JsonResponse(data)
            else:
                data = {
                    'msg_insufficient': 'Insufficient funds'  # response message
                }
                return JsonResponse(data)
        else:
            data = {
                'msg_wrong_password': 'You have inputted a wrong password.'  # response message
            }
            return JsonResponse(data)


@login_required
@api_view(["GET", "POST"])
def ajax_all_order(request):
    vendor = request.user.vendor
    all_order = Order.objects.filter(vendor=vendor, ordered=True).order_by("-date_posted")
    data = OrderSerializer(all_order, many=True).data

    return Response(data)
