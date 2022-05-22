from django.shortcuts import render
from matplotlib.style import context
from numpy import product
from store.models import Product


# Create your views here.
def store_home(request):
    products = Product.objects.filter(is_available = True)
    products_count = products.count()
    context_date ={
        'products':products,
        'products_count': products_count
    }
    return render(request,'store/store.html',context_date)