from django.contrib import admin
from store.models import Product
# Register your models here.

class Product_admin(admin.ModelAdmin):
    list_display = ['product_name','price','stock','is_available','category']

admin.site.register(Product,Product_admin)