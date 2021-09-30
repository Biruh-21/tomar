from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import SignupForm, UserUpdateForm, ProfileUpdateForm


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
def profile(request):
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
            return redirect("blog:blog-home")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "account/profile_update.html", context)
