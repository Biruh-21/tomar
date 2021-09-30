from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    """Category of posts written for ease of reading."""

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    """Posts written by users or admin."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)  # automatically generate from title
    content = models.TextField()
    date_posted = models.DateTimeField(timezone.now())
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title
