from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control py-4', 'placeholder': "Введите пароль"}
    ))

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control py-4', 'placeholder': 'Введите имя'}
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control py-4', 'placeholder': 'Введите фамилию'}
    ))
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}
    ))
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control py-4', 'placeholder': 'Введите адрес эл. почты'}
    ))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control py-4', 'placeholder': 'Введите пароль'}
    ))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(
        attrs={'class': 'form-control py-4', 'placeholder': 'Подтвердите пароль'}
    ))

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'custom-file-input'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', "readonly": True}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', "readonly": True}))

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'image', 'username', 'email')
