from django.shortcuts import render
from django.views import generic

from .models import Post


class HomePageView(generic.ListView):
    template_name = "blog/index.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.all()


def index(request):
    """Show the home page of the website."""
    featured_posts = Post.objects.all()[:4]
    all_posts = Post.objects.all()[5:]
    context = {
        "featured_posts": featured_posts,
        "all_posts": all_posts,
    }
    return render(request, "blog/index.html", context)


class PostDetailView(generic.DetailView):
    model = Post
    context_object_name = "post"


def post_detail(request):
    """A one post view while the user is reading."""
    return render(request, "blog/post.html")
