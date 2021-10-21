from django.contrib import admin

from account.models import Account, Profile


admin.site.register(Profile)
admin.site.register(Account)
