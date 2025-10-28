from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from products.models import Product
from products.serializers import ProductSerializer


class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
