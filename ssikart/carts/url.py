from django.contrib import admin
from django.urls import path

from carts.views import add_cart, cart, checkout, remove_cart, remove_cart_item

urlpatterns = [
    path("", cart, name="ssi-cart"),
    path('checkout/',checkout, name='checkout'),
    path('add_cart/<int:product_id>', add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>', remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>', remove_cart_item, name='remove_cart_item'),
]
