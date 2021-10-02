from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

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

    def form_valid(self, form):
        form.instance.user = self.request.user  # assign post author
        return super().form_valid(form)
