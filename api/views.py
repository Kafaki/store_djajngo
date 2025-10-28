from rest_framework.generics import ListAPIView

from products.models import Product
from products.serializers import ProductSerializer


class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()
