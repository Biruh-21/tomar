from django.contrib import admin

from .models import Category, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "date_posted", "category", "author")
    list_filter = ("date_posted", "category", "author")
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
