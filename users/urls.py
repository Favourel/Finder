from django.urls import path
from . import views as user_view
from users.middlewares.auth import LogoutCheckMiddleware

urlpatterns = [
    path("register/", LogoutCheckMiddleware(user_view.register), name="register"),
    path("vendor/<str:username>/", user_view.vendor_view, name="vendor"),
    path("dashboard/", user_view.vendor_dashboard, name="vendor_dashboard"),
    path('update-profile/', user_view.update_profile, name='update_profile'),
    path("notification/", user_view.notification_view, name="notification"),
    path("create-store/", user_view.create_store, name="create_store"),
    path("<str:username>/follow", user_view.UserFollowerApi.as_view(), name="follower_vendor"),
    path('api/<str:username>/post_notify/', user_view.PostNotificationApi.as_view(), name='post_notify'),
    path('update_notification/', user_view.update_notification, name='update_notification'),
    path('settings/', user_view.settings, name='settings'),

]