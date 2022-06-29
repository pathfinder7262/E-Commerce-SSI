from operator import ipow
from django.urls import URLPattern, path
from accounts.views import login,logout,register    

urlpatterns = [
    path('register/',register,name='registration'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    ]


