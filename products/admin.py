from django.contrib import admin
from .models import Product, Variation

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category_lvl_one', 'product_sku')
    prepopulated_fields = {'slug':('product_sku',)}

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_name', 'price', 'stock', 'is_active',)
    list_filter = ('product', 'variation_name', 'price', 'stock', 'is_active',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)