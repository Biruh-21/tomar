from django.shortcuts import render
from django.views import generic

from .models import Post


class HomePageView(generic.ListView):
    template_name = "blog/home.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.all()


# def index(request):
#     """Show the home page of the website."""
#     return render(request, "blog/home.html")


class PostDetailView(generic.DetailView):
    model = Post
    context_object_name = "post"


def post_detail(request):
    """A one post view while the user is reading."""
    return render(request, "blog/post_detail.html")
