from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .bulma_mixin import BulmaMixin
from .models import User


class EmailForm(BulmaMixin, forms.Form):
    email = forms.EmailField(label='Введите адрес почты')

    class Meta:
        model = User
        fields = ['email']


class AuthForm(BulmaMixin, forms.Form):
    code = forms.CharField(label='Введите код')

    class Meta:
        model = User
        fields = ['code']


class EditProfileForm(BulmaMixin, forms.ModelForm):
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    username = forms.CharField(label='Никнейм')
    email = forms.EmailField(label='Адрес почты')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class ResetPasswordForm(BulmaMixin, PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(), label='Текущий пароль')
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(), label='Новый пароль')
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(), label='Повторите новый пароль'
    )

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
