from django.contrib import admin
from store.models import Product
# Register your models here.

class Product_admin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('product_name',)
    }
    list_display = ['product_name','price','stock','is_available','category']

admin.site.register(Product,Product_admin)