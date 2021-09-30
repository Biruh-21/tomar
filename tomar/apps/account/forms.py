from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import UserProfile


class SignupForm(UserCreationForm):
    """Form used to register the user."""

    email = forms.EmailField()

    # what is Meta class? what it does?
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    """A Form used to update user information."""

    class Meta:
        model = User
        fields = ["username"]


class ProfileUpdateForm(forms.ModelForm):
    """A Form used to update profile of the user."""

    class Meta:
        model = UserProfile
        fields = ["bio", "about", "profile_picture"]
