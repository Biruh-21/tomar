from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="account/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="blog:post-list"),
        name="logout",
    ),
    path("<str:username>/about/", views.about_user, name="about-user"),
    path("<str:username>/profile/", views.UserPostListView.as_view(), name="profile"),
    path("<str:username>/update/", views.update_profile, name="profile-update"),
]
