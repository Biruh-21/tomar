from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import View, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from accounts.models import Account
from .models import Bookmark, Comment, Post
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
        # bookmarks = Bookmark.objects.filter(user=user)
        bookmarks = user.bookmarks.all()
        saved_posts = []
        for bookmark in bookmarks:
            saved_posts.append(bookmark.post)
    else:
        saved_posts = []

    context = {
        "featured_posts": featured_posts,
        "all_posts": all_posts,
        "saved_posts": saved_posts,
    }
    return render(request, "blog/index.html", context)


class PostDetailView(DetailView):
    """Show the detail of a single post."""

    model = Post
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.post = get_object_or_404(Post, slug=self.kwargs.get("slug"))
        self.is_bookmarked = False
        if self.request.user.pk is not None:
            user = Account.objects.get(id=self.request.user.pk)
            bookmarks = user.bookmarks.all()
            saved_posts = []
            for bookmark in bookmarks:
                saved_posts.append(bookmark.post)
        context["saved_posts"] = saved_posts
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


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Display comment creation form and handle the commenting process."""

    model = Comment
    fields = ["content"]
    template_name = "blog/comments.html"

    # def get_queryset(self):
    #     return None

    def form_valid(self, form):
        # assign the current logged in user as author of the comment
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(slug=self.kwargs.get("slug"))
        return super().form_valid(form)

    def get_queryset(self):
        return Comment.objects.all()


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


class BookmarkPost(LoginRequiredMixin, View):
    """Handle bookmarking post using ajax calls."""

    def post(self, request):
        user_id = self.request.user.pk
        post_id = request.POST.get("post_id")
        if user_id is not None:
            # the user is authenticated, go to bookmark activity
            user = Account.objects.get(pk=user_id)
            post = Post.objects.get(pk=post_id)
            is_bookmarked = Bookmark.objects.filter(user=user, post=post).exists()
            # print(post_id)
            # print(user_id)
            # print(is_bookmarked)
            if is_bookmarked:
                # remove the post from his bookmark
                Bookmark.objects.filter(user=user, post=post).delete()
                is_bookmarked = False
            else:
                # add to his bookmark list
                Bookmark.objects.create(user=user, post=post)
                is_bookmarked = True
            data = {"is_bookmarked": is_bookmarked, "button_val": post_id}
            return JsonResponse(data, status=200)
        else:
            data = {"is_bookmarked": False, "button_val": post_id}
            return JsonResponse(data, status=200)


@login_required
def bookmark_post(request, slug, pk):
    """Bookmark the post for later reading."""
    selected_post = get_object_or_404(Post, slug=slug)
    if Bookmark.objects.filter(id=request.user.pk).exists():
        Bookmark.objects.delete(user_id=request.user.pk, post_id=selected_post.pk)
        messages.warning(request, "Removed from saved posts")
    else:
        Bookmark.objects.create(user_id=request.user.pk, post_id=selected_post.pk)
        messages.success(request, "Added to your saved posts.")

    # return HttpResponseRedirect(reverse("blog:post-list"))
