from django.contrib import admin
from .models import ProductItem, ProductImage, Category


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of extra forms to display


class ProductItemAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('name','product_code', 'category', 'price', 'quantity_in_stock', 'out_of_stock')
    list_filter = ('category', 'out_of_stock')
    search_fields = ('name', 'product_code', 'category')


admin.site.register(ProductItem, ProductItemAdmin)
admin.site.register(ProductImage)
admin.site.register(Category)