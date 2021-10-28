from django.contrib import admin

from .models import Category, Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "date_posted", "category", "author")
    list_filter = ("date_posted", "category", "author")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "content", "date_posted")
    list_filter = ("date_posted", "author")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}
