from django.shortcuts import render


def index(request):
    """Show the home page of the website."""
    return render(request, "blog/home.html")


def post_detail(request):
    """A one post view while the user is reading."""
    return render(request, "blog/post_detail.html")
