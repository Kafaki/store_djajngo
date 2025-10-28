from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'api'

router = routers.SimpleRouter()
router.register(r'products', views.ProductModelViewSet, )


urlpatterns = [
    path('', include(router.urls)),
    path('test-product-list/', views.ProductListAPIView.as_view(), name='product_list'),
]
