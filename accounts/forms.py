from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Address, CustomUser


class CustomUserLoginForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['city', 'street', 'house_number', 'zipcode', 'country']


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name",
                  "email", "user_type", "phone")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")
