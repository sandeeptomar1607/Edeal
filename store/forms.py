from django import forms
from django.contrib.auth.forms import UserCreationForm

from store.models import Product, User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "mobile",
            "role",
            "password1",
            "password2",
        )


# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ("category", "name", "price", "description", "image")
