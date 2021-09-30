from django.contrib import admin

from .models import Category, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "date_posted", "category", "user")
    list_filter = ("date_posted", "category", "user")
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
