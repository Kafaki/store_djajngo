from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from products.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib import messages


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return redirect('products:index')
    else:
        form = UserLoginForm()

    return render(request, template_name='users/login.html', context={'form': form})


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')


# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Аккаунт зарегистрирован ')
#             return redirect("users:login")
#     else:
#         form = UserRegistrationForm()
#
#     return render(request, template_name='users/registration.html', context={"form": form})


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Store - Профиль'
        context['baskets'] = self.request.user.baskets.all()  # Использование related_name
        # или context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user,
#                                data=request.POST,
#                                files=request.FILES
#                                )
#         if form.is_valid():
#             form.save()
#             return redirect("users:profile")
#     else:
#         form = UserProfileForm(instance=request.user)
#
#     data = {
#         'titile': 'Store - Профиль',
#         "form": form,
#         'baskets': Basket.objects.filter(user=request.user),
#     }
#
#     return render(request, template_name='users/profile.html',
#                   context=data)
