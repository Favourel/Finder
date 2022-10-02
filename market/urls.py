from django.urls import path, re_path
from . import views as market_view


urlpatterns = [
    path("", market_view.home, name="home"),
    path("market/", market_view.market_view, name="market"),
    path("product/<int:pk>/", market_view.product_detail, name="product-detail"),
    path("<int:pk>/add_to_checkout/", market_view.add_to_checkout, name="add_to_checkout"),
    path("<int:pk>/remove_from_checkout/", market_view.remove_from_checkout, name="remove_from_checkout"),
    path("checkout/", market_view.checkout, name="checkout"),
    path("product/<int:pk>/update/", market_view.update_product, name="product-update"),
    path("product/<int:pk>/review/", market_view.productReview, name="productReview"),
    path("create/", market_view.create_view, name="create"),
    path("search/", market_view.search, name="search"),
    path("<str:username>/follow", market_view.UserFollowerApi.as_view(), name="follower_vendor"),
    path('api/<str:username>/post_notify/', market_view.PostNotificationApi.as_view(), name='post_notify'),

]