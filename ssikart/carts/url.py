
from django.conf import settings
from django.contrib import admin
from django.urls import path
from carts.views import cart




urlpatterns = [
    path('',cart,name='ssi-cart')
    
]

