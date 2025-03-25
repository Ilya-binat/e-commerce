from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("product/<int:pk>", views.product, name="product"),
    path("guest_register/<int:pk>", views.guest_register, name="guest_register"),
    path("cart/", views.cart, name="cart"),
    path("create_order/", views.create_order, name="create_order"),
    path("favorite/<int:pk>", views.favorite, name="favorite"),
    path("favorite_page/", views.favorite_page, name="favorite_page"),
    path("orders/", views.orders, name="orders"),
    path("order_delete/<int:pk>", views.order_delete, name="delete_order"),
    path("order_edit/<int:pk>", views.order_edit, name="order_edit"),
]
