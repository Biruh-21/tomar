from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="blog-home"),
    path("post/new/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="post-detail"),
]
