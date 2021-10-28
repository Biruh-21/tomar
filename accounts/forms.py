from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Account, Profile


class SignupForm(UserCreationForm):
    """Form used to register the user."""

    class Meta:
        model = Account
        fields = ["email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    """A Form used to update user information."""

    class Meta:
        model = Account
        fields = ["first_name", "last_name"]


class ProfileUpdateForm(forms.ModelForm):
    """A Form used to update profile of the user."""

    class Meta:
        model = Profile
        fields = ["bio", "about", "avator"]
