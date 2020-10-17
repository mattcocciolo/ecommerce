from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Order, Customer, ShippingAddress


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario...'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email...'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre...'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido...'}),
        }

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password...'}))

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Password...'}))


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', 'name']


class ShippingForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = '__all__'
        exclude = ['customer', 'order']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Direccion...'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad...'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Provincia...'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Codigo Postal...'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pais...'}),
        }


