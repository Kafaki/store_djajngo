from django.shortcuts import render, redirect
from .models import ProductCategory, Product, Basket


# Create your views here.
def index(request):
    context = {
        'title': 'Store',
    }
    return render(request, 'products/index.html', context=context)


def products(request):
    context = {
        'title': 'Store - Каталог',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all()
               }
    return render(request, 'products/products.html', context=context)


def basket_add(request, product_id):
    product = Product.objects.get(pk=product_id)
    basket = Basket.objects.filter(user=request.user, product=product)

    if not basket.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = basket.first()
        basket.quantity += 1
        basket.save()
    return redirect(request.META['HTTP_REFERER'])

def basket_remove(request, basket_id):
    basket = Basket.objects.get(pk=basket_id)
    basket.delete()
    return redirect(request.META['HTTP_REFERER'])