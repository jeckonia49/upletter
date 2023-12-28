from django.urls import path
from . import views

app_name = "shops"

urlpatterns = [
    path("", views.ShopView.as_view(), name="shop_view"),
    path("cart/", views.CartListView.as_view(), name="cart_view"),
    path("cart/place-order/", views.CartCheckoutView.as_view(), name="place_order"),
    path("<product_slug>/", views.ShopProductDetailView.as_view(), name="product_detail"),
    path("<product_slug>/write-review/", views.ProductReviewView.as_view(), name="product_review"),
    path("<product_slug>/add-to-cart/", views.AddProductToCartView.as_view(), name="product_add_to_cart"),
    path("<product_slug>/remove_from-cart/", views.RemoveProductFromCartView.as_view(), name="product_remove_from_cart"),
]
