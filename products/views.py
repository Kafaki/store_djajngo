from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .models import ProductCategory, Product, Basket


class IndexView(TemplateView):
    template_name = 'products/index.html'
    extra_context = {'title': 'Store'}


def products(request, category_id=None, page_number=1):
    prods = Product.objects.filter(category__id=category_id) if category_id else Product.objects.all()
    per_page = 3
    paginator = Paginator(prods, per_page)
    prods_paginator = paginator.get_page(page_number)

    context = {
        'title': 'Store - Каталог',
        'categories': ProductCategory.objects.all(),
        'products': prods_paginator
    }
    return render(request, 'products/products.html', context=context)


@login_required
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
