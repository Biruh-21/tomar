from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("confirm/<uidb64>/<token>/", views.activate, name="activate"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="blog:post-list"),
        name="logout",
    ),
    path("follow/", views.FollowView.as_view(), name="follow"),
    path(
        "<str:display_name>/profile/", views.UserProfileView.as_view(), name="profile"
    ),
    path("<str:display_name>/saved/", views.SavedPostListView.as_view(), name="saved"),
    path("<str:display_name>/about/", views.about_user, name="about-user"),
    path("<str:display_name>/update/", views.update_profile, name="profile-update"),
    path("<str:display_name>/settings/", views.settings, name="settings"),
]
