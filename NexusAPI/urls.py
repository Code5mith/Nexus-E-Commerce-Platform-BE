from django.urls import path
from . import views

urlpatterns = [
    path("products", views.product_list, name="product_list"),
    path("product/<slug:slug>", views.product_detail, name="product_detail"),
    path("categories", views.category_list, name="category_list"),
    path("category/<slug:slug>", views.category_detail, name="category_detail"),
    path("add_to_cart/", views.add_to_cart, name="add_to_cart"),
    path("update_cartitem-quantity/", views.update_cart_item_quantity, name="update_cartitem_quantity"),
]