from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from .forms import SignupForm, UserUpdateForm, ProfileUpdateForm
from blog.models import Post
from account.models import Account


def signup(request):
    """Display signup form and handle the signup action."""

    if request.method == "POST":
        # the user has submitted the form (POST request): get the data submitted
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            messages.success(request, "Your account has been created successfully.")
            # TODO add email verification
            signup_form.save()
            return redirect("account:login")
    else:
        # it is GET request: display an empty signup form
        signup_form = SignupForm()

    context = {"signup_form": signup_form}
    return render(request, "account/signup.html", context)


@login_required
def update_profile(request, display_name):
    """Show profile for authenticated user."""
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your account has been updated successfully.")
            return redirect(to=reverse("account:profile", args=(display_name,)))
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "account/profile_update_form.html", context)


# def profile(request, username):
#     """Show author's profile and his/her posts."""

#     user = get_object_or_404(User, username=username)
#     user_posts = Post.objects.filter(user=user)

#     context = {
#         "user": user,
#         "user_posts": user_posts,
#     }
#     return render(request, "account/profile.html", context)


class UserPostListView(ListView):
    """Show profile of the user and all posts posted by the user."""

    context_object_name = "user_posts"
    template_name = "account/user_profile.html"

    def get_queryset(self):
        # Filtering posts by the user only
        self.user = get_object_or_404(
            Account, display_name=self.kwargs.get("display_name")
        )
        return Post.objects.filter(author=self.user).order_by("-date_posted")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.user
        return context


class SavedPostListView(ListView):
    """Show saved posts by the user."""

    model = settings.AUTH_USER_MODEL
    context_object_name = "saved_posts"
    template_name = "blog/saved_posts.html"

    def get_queryset(self):
        user = get_object_or_404(Account, display_name=self.kwargs.get("display_name"))
        return user.bookmark.all()


def about_user(request, display_name):
    """Show about of the user."""
    user = Account.objects.get(display_name=display_name)
    return render(request, "account/about_user.html", {"user": user})
