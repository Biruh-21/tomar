from django.shortcuts import render


def index(request):
    """Show the home page of the website."""
    return render(request, "blog/home.html")
