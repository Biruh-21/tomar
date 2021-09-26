from django.urls import path
from django.contrib.auth import views as auth_views

from . import views as account_views

app_name = "account"

urlpatterns = [
    path("signup/", account_views.signup, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="account/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
