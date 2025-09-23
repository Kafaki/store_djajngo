from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from users.forms import UserLoginForm


# Create your views here.

def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user and user.is_active:
                print('done')
                login(request, user)
                return redirect('products:index')
    else:
        form = UserLoginForm()

    return render(request, template_name='users/login.html', context={'form': form})




def registration(request):
    return render(request, template_name='users/registration.html', )
