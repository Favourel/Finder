from django.contrib import admin
from users.models import User, Notification
# from django.contrib.auth.admin import UserAdmin
# from .forms import UserRegisterForm

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', "is_verified")
    search_fields = ('username', 'email')

# class CustomerAdmin(UserAdmin):
#     add_form = UserRegisterForm
#     model = User
#     list_display = ('username', 'email', 'date_joined', "is_verified")


class NotificationAdmin(admin.ModelAdmin):
    list_display = ["sender", "notification_type", "user", "date_posted", "is_seen"]


admin.site.register(User, UserAdmin)
admin.site.register(Notification, NotificationAdmin)
