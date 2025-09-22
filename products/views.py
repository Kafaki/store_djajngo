from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, template_name='products/index.html', )


def products(request):
    return render(request, template_name='products/products.html', )
