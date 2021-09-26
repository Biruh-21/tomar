from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import SignupForm


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
