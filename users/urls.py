from django.urls import path
from . import views as user_view
from users.middlewares.auth import LogoutCheckMiddleware

urlpatterns = [
    path("register/", LogoutCheckMiddleware(user_view.register), name="register"),
    path("<str:username>/vendor/", user_view.vendor_view, name="vendor"),
    path('update-profile/', user_view.update_profile, name='update_profile'),
    path("notification/", user_view.notification_view, name="notification"),
    path("create-store/", user_view.create_store, name="create_store"),
]