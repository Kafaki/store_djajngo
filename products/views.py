from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView

from common.views import TitleMixin

from .models import Basket, Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'  # передаем аргумент через миксин TitleMixin


class ProductsView(ListView):
    template_name = 'products/products.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data()
        context['title'] = 'Store - Каталог'
        context['categories'] = ProductCategory.objects.all()
        return context

    def get_queryset(self):
        category_id = self.kwargs.get('category_id', None)

        if category_id:
            return Product.objects.filter(category__id=category_id)
        return Product.objects.all()


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
