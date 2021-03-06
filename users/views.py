from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import auth
from .forms import *
from django.contrib import messages
from .models import *
from market.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


# Create your views here.


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form_password = form.clean_password2()
            form = form.save(commit=False)
            email = form.email
            if User.objects.filter(email=email).exists():
                messages.error(request, "email already exists")
                return redirect("register")
            else:
                form.save()
                username = form.username
                password = form.password
                print(username, password)

                auth_login = auth.authenticate(username=username, password=form_password)
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
        notification = Notification.objects.filter(user=request.user, is_seen=False)[:3]
        notification_count = Notification.objects.filter(user=request.user, is_seen=False).count()
        if request.method == 'POST':
            u_form = StoreCreateForm(request.POST)
            education_field = StoreCreateFormEducationField(request.POST)

            if u_form.is_valid():
                u_form = u_form.save(commit=False)
                # education_field = education_field.save(commit=False)
                u_form.user = request.user
                # education_field.user = request.user
                u_form.save()
                # education_field.save()

                messages.success(request, f'Your store has been created by {user}.')
                return redirect('create')
        else:
            u_form = StoreCreateForm()

        context = {
            'u_form': u_form,
            "education_field": StoreCreateFormEducationField(),
            "notification_count": notification_count,
            "notification": notification
        }
        return render(request, 'users/create_store.html', context)
    else:
        messages.warning(request, 'You are already a vendor')
        return redirect(f'/{user}/vendor/')


@login_required
def vendor_view(request, username):
    try:
        notification = Notification.objects.filter(user=request.user, is_seen=False).order_by("-id")[:3]
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
        "form": UserUpdateForm(instance=request.user)
    }
    return render(request, "users/vendor_post.html", context)


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
    notification = Notification.objects.filter(user=request.user, is_seen=False)[:3]
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

            # "queryset": queryset
        }
        return render(request, "users/notification.html", context)
    else:
        notification_list = Notification.objects.filter(user=request.user).order_by("-date_posted").exclude(notification_type=7)
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

        }
        return render(request, "users/notification.html", context)
