from django.contrib.auth import authenticate, login, tokens
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import ListView
from django.views.generic.base import View

from .tokens import email_confirmation_token
from .forms import SignupForm, UserUpdateForm, ProfileUpdateForm
from .models import Account, Profile
from blog.models import Post


def signup(request):
    """Display signup form and handle the signup action."""

    if request.method == "POST":
        # the user has submitted the form (POST request): get the data submitted
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.is_active = False  # until the user confirms the email
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Tomar: Confirm your email address"
            message = render_to_string(
                "accounts/confirm_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": email_confirmation_token.make_token(user),
                },
            )
            to_email = signup_form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            messages.info(
                request,
                "Please confirm your email address to complete the registration.",
            )
            messages.info(
                request,
                "Confirmation link has been sent to the email address you provide.",
            )
            # # Automatically log the user in
            # user = authenticate(
            #     request,
            #     email=signup_form.cleaned_data["email"],
            #     password=signup_form.cleaned_data["password1"],
            # )
            # login(request, user)
            return redirect("blog:post-list")
    else:
        # it is GET request: display an empty signup form
        signup_form = SignupForm()

    context = {"signup_form": signup_form}
    return render(request, "accounts/signup.html", context)


def activate(request, uidb64, token):
    """Activate the user account after the confirms their email address."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and email_confirmation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Your email has been verified successfully.")
        messages.success(
            request, "You can now write posts and share your idea to the world."
        )
        return redirect("blog:post-list")
    else:
        return HttpResponse("Confirmation link is invalid.")


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
            return redirect(to=reverse("accounts:profile", args=(display_name,)))
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "accounts/profile_update_form.html", context)


class UserProfileView(ListView):
    """Show profile of the user and all posts posted by the user."""

    context_object_name = "user_posts"
    template_name = "accounts/user_profile.html"

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


class SavedPostListView(LoginRequiredMixin, ListView):
    """Show saved posts by the user."""

    model = Account
    context_object_name = "saved_posts"
    template_name = "blog/saved_posts.html"

    def get_queryset(self):
        user = Account.objects.get(id=self.request.user.pk)
        saved_posts = [post for post in user.bookmarks.all()]
        return saved_posts


class FollowView(View):
    """Handle Follow and Unfollow process."""

    def post(self, request):
        current_user = self.request.user  # the user making the request
        if current_user.is_authenticated:
            user_id = request.POST["user_id"]  # the user to follow or unfollow
            user_profile = Profile.objects.get(user__id=user_id)
            following = False
            if not user_profile.user in current_user.profile.following_list:
                current_user.profile.following.add(user_profile)
                following = True
            else:
                current_user.profile.following.remove(user_profile)

            return JsonResponse({"following": following}, status=200)
        else:
            messages.info(
                self.request,
                "Login to your account to follow other users.",
            )
            return JsonResponse({"not_authenticated": True}, status=401)


def about_user(request, display_name):
    """Show about of the user."""
    user = Account.objects.get(display_name=display_name)
    return render(request, "accounts/about_user.html", {"user": user})
