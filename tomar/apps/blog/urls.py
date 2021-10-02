from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    # path("", views.HomePageView.as_view(), name="blog-home"),
    path("", views.index, name="blog-home"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="post-detail"),
    # path("post/", views.post_detail, name="post-detail"),
]
