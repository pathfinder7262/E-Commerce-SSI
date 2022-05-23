from django.http import HttpResponse
from django.shortcuts import render
from store.models import Product


# Create your views here.
def main_home(request):
    ''' This line product is derived from db '''
    products = Product.objects.filter(is_available = True)
    context_date = {
        "products" : products,
    }

    return render(request,'home/index.html',context_date)