from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="post-list"),
    path("bookmark/", views.BookmarkPost.as_view(), name="bookmark"),
    path("post/write/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="post-detail"),
    path(
        "post/<slug:slug>/update/", views.PostUpdateView.as_view(), name="post-update"
    ),
    path(
        "post/<slug:slug>/delete/", views.PostDeleteView.as_view(), name="post-delete"
    ),
    path("post/<slug:slug>/comments/", views.comments, name="comment"),
]
