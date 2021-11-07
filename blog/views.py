from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from accounts.models import Account
from .models import Comment, Post
from .forms import CommentForm


# class HomePageView(generic.ListView):
#     """Show the home page of the website."""
#     template_name = "blog/index.html"
#     context_object_name = "posts"

#     def get_queryset(self):
#         return Post.objects.all()


def index(request):
    """Show the home page of the website."""
    featured_posts = Post.objects.all().order_by("-date_posted")[:4]
    all_posts = Post.objects.all()[4:]
    if request.user.pk is not None:
        user = Account.objects.get(id=request.user.pk)
        saved_posts = [post for post in user.bookmarks.all()]
        user_feed = Post.objects.all()
    else:
        saved_posts = []
        user_feed = []

    if request.user.pk is not None:
        context = {
            "user_feed": user_feed,
            "saved_posts": saved_posts,
        }
        return render(request, "blog/index.html", context)
    else:
        context = {
            "featured_posts": featured_posts,
        }
        return render(request, "blog/landing-page.html", context)


class PostDetailView(DetailView):
    """Show the detail of a single post."""

    model = Post
    context_object_name = "post"
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.post = get_object_or_404(Post, slug=self.kwargs.get("slug"))
        is_bookmarked = False
        is_liked = False
        if self.request.user.pk is not None:
            user = Account.objects.get(id=self.request.user.pk)
            if user in self.post.bookmarkers_list:
                is_bookmarked = True
            if user in self.post.likers_list:
                is_liked = True

        context["is_bookmarked"] = is_bookmarked
        context["is_liked"] = is_liked
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Display post creation form and handle the process."""

    model = Post
    fields = ["category", "title", "content", "image"]
    template_name = "blog/post_create_form.html"

    def form_valid(self, form):
        # assign the current logged in user as author of the post
        form.instance.author = self.request.user
        messages.success(
            self.request,
            "You have published a new post. You can edit or delete it anytime.",
        )
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Display post update form and handle the process."""

    model = Post
    fields = ["category", "title", "content", "image"]
    template_name = "blog/post_update_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Your post have been updated.")
        return super().form_valid(form)

    def test_func(self):
        # check that the person trying to update the post is owner of the post
        return self.get_object().author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Display post deletion form and handle the process."""

    model = Post

    def get_success_url(self):
        # After deleting the post, redirect to user's profile page
        messages.success(self.request, "Your post has been delete permanently.")
        post_slug = self.kwargs["slug"]
        author = Post.objects.get(slug=post_slug).author
        return reverse_lazy("accounts:profile", args=(author.display_name,))

    def test_func(self):
        # check that the person trying to delete the post is owner of the post
        return self.get_object().author == self.request.user


class CategoryView(ListView):
    """Show all post in a certain category."""

    model = Post
    template_name = "blog/category.html"
    context_object_name = "category_posts"

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs.get("slug"))


def comments(request, slug):
    """Manages comments on posts."""
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # comment_form.save(commit=False)
            comment_form.instance.author = request.user
            comment_form.instance.post = post
            comment_form.save()

    comment_form = CommentForm()

    context = {"comment_form": comment_form, "comments": post.comments.all()}
    return render(request, "blog/comments.html", context)


class BookmarkPost(View):
    """Handle bookmarking post using ajax calls."""

    def post(self, request):
        user_id = self.request.user.pk
        post_id = request.POST.get("post_id")
        if user_id is not None:
            # the user is authenticated, go to bookmark activity
            user = Account.objects.get(pk=user_id)
            post = Post.objects.get(pk=post_id)
            is_bookmarked = False
            if not user in post.bookmarkers_list:
                post.bookmark.add(user)
                is_bookmarked = True
            else:
                post.bookmark.remove(user)
            return JsonResponse({"is_bookmarked": is_bookmarked}, status=200)
        else:
            messages.info(
                self.request,
                "Login to your account to bookmark posts for later reading.",
            )
            return JsonResponse({"is_bookmarked": False}, status=401)


class LikePost(View):
    """Handle bookmarking post using ajax calls."""

    def post(self, request):
        user_id = self.request.user.pk
        post_id = request.POST.get("post_id")
        if user_id is not None:
            # the user is authenticated, go to like activity
            user = Account.objects.get(pk=user_id)
            post = Post.objects.get(pk=post_id)
            is_liked = False
            if not user in post.likers_list:
                post.likes.add(user)
                is_liked = True
            else:
                post.likes.remove(user)

            data = {"is_liked": is_liked, "button_val": post_id}
            return JsonResponse(data, status=200)
        else:
            messages.info(
                self.request,
                "Login to your account to like posts.",
            )
            data = {"is_liked": False, "button_val": post_id}
            return JsonResponse(data, status=401)
