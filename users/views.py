from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from products.models import Basket
# from products.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User, EmailVerification


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('products:index')
# def login_user(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'], password=cd['password'])
#             if user and user.is_active:
#                 login(request, user)
#                 return redirect('products:index')
#     else:
#         form = UserLoginForm()
#
#     return render(request, template_name='users/login.html', context={'form': form})


class UserRegistrationView(SuccessMessageMixin,CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    extra_context = {'title': 'Регистрация',}
    success_message = 'Аккаунт зарегистрирован'


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
        context['baskets'] = Basket.objects.filter(user=self.request.user)
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


class EmailVerificationView(TemplateView):
    extra_context = {'title': 'Store - Подтверждение электронной почты', }
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = self.kwargs['code']
        user = User.objects.get(email=self.kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super().get(request, *args, **kwargs)
        else:
            return  redirect('products:index')

