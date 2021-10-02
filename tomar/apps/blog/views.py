from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import request
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Post


# class HomePageView(generic.ListView):
#     template_name = "blog/index.html"
#     context_object_name = "posts"

#     def get_queryset(self):
#         return Post.objects.all()


def index(request):
    """Show the home page of the website."""
    featured_posts = Post.objects.all()[:4]
    all_posts = Post.objects.all()[5:]
    context = {
        "featured_posts": featured_posts,
        "all_posts": all_posts,
    }
    return render(request, "blog/index.html", context)


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    """Display post creation form and handle post creation."""

    model = Post
    fields = ["category", "title", "content", "summary", "image"]
    template_name = "blog/post_create_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user  # assign post author
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Display post update form and handle post update."""

    model = Post
    fields = ["category", "title", "content", "summary", "image"]
    template_name = "blog/post_update_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user  # assign post author
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Display post deletion form and handle post deletion."""

    model = Post

    def get_success_url(self):
        post_slug = self.kwargs["slug"]
        user = Post.objects.get(slug=post_slug).user
        return reverse_lazy("account:profile", args=(user.username,))

    def test_func(self):
        return self.get_object().user == self.request.user
