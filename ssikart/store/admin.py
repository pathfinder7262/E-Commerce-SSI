from django.contrib import admin
from store.models import Product,Variation
# Register your models here.

class Product_admin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('product_name',)
    }
    list_display = ['product_name','price','stock','is_available','category']

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    list_editable = ('is_active',)
    list_filter = ('product' , 'variation_category' , 'variation_value')



admin.site.register(Product,Product_admin)
admin.site.register(Variation,VariationAdmin)