from django.urls import path, re_path
from . import views as market_view


urlpatterns = [
    path("", market_view.home, name="home"),
    path("market/", market_view.market_view, name="market"),
    path("paginate_products/", market_view.paginate_products, name="paginate_products"),
    path("product/<uuid:pk>/", market_view.product_detail, name="product-detail"),
    path("<uuid:pk>/add_to_checkout/", market_view.add_to_checkout, name="add_to_checkout"),
    path("<uuid:pk>/remove_from_checkout/", market_view.remove_from_checkout, name="remove_from_checkout"),
    path("<uuid:pk>/delete_from_checkout/", market_view.delete_from_checkout, name="delete_from_checkout"),
    path("checkout/", market_view.checkout, name="checkout"),
    path("process_order/", market_view.process_order, name="process_order"),
    path("product/<uuid:pk>/update/", market_view.update_product, name="product-update"),
    path("product/<uuid:pk>/review/", market_view.product_review, name="productReview"),
    path("create/", market_view.create_view, name="create"),
    path("search/", market_view.search, name="search"),

]