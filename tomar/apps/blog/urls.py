from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="blog-home"),
    path("<slug>/", views.post_detail, name="post-detail"),
]
