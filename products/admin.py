from django.contrib import admin

from products.models import Product, ProductCategory


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    ...

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    ...