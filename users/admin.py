from django.contrib import admin
from users.models import User, Notification
# from django.contrib.auth.admin import UserAdmin
# from .forms import UserRegisterForm
from django.db.models import F

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', "is_verified")
    search_fields = ('username', 'email')
    filter_horizontal = ['following', 'follower', "post_notification"]
    list_per_page = 15


class NotificationAdmin(admin.ModelAdmin):
    list_display = ["sender", "notification_type", "user", "date_posted", "is_seen"]
    actions = ["mark_as_unread"]
    list_per_page = 15

    def mark_as_unread(self, request, queryset):
        queryset.update(is_seen=F('is_seen') == True)
        self.message_user(request,
                          "Marked as unread for {} notifications".format([i.user for i in queryset]))

    mark_as_unread.short_description = 'Mark as unread'


admin.site.register(User, UserAdmin)
admin.site.register(Notification, NotificationAdmin)
