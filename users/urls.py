from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('products/', views.registration, name='registration'),

    path('logout/', LogoutView.as_view(next_page='products:index'), name='logout'),

]
