from operator import ipow
from django.urls import URLPattern, path
from accounts.views import register,login,logout,dashboard  

urlpatterns = [
    path('register/',register,name='registration'),
    path('login/',login,name='login'),
    path("dashboard/", dashboard, name="dashboard"),
    path('logout/',logout,name='logout'),
    ]


