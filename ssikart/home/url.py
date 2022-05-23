from django import views
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.main_home ,name = "ssi-main-home"),
]
