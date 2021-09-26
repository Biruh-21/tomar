from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignupForm(UserCreationForm):

    email = forms.EmailField()

    # what is Meta class? what it does?
    class Meta:
        model = User
        fields = ["username", "email", "password1"]
