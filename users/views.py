from django.shortcuts import render

# Create your views here.

def login(request):
    return  render(request, template_name='users/login.html', )


def registration(request):
    return  render(request, template_name='users/registration.html', )