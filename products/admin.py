from django.contrib import admin

from products.models import Basket, Product, ProductCategory


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category', 'id')
    fields = ('image', 'name', 'description', ('price', 'quantity'), 'stripe_product_price_id', 'category')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    ...


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')
    readonly_fields = ('created_timestamp',)
