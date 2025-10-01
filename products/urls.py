from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('products/', views.ProductsView.as_view(), name='products'),
    path('products/category/<int:category_id>', views.ProductsView.as_view(), name='category'),

    path('products/baskets/add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('products/baskets/remove/<int:basket_id>/', views.basket_remove, name='basket_remove')

]
