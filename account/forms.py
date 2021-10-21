from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Profile


class SignupForm(UserCreationForm):
    """Form used to register the user."""

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    """A Form used to update user information."""

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]


class ProfileUpdateForm(forms.ModelForm):
    """A Form used to update profile of the user."""

    class Meta:
        model = Profile
        fields = ["bio", "about", "profile_picture"]
