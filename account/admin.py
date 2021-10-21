from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from account.models import Account, Profile


class UserCreationForm(forms.ModelForm):
    pass


admin.site.register(Profile)
admin.site.register(Account)
