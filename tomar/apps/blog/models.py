from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse


class Category(models.Model):
    """Category of posts written for ease of reading."""

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    """Posts written by users or admin."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)  # automatically generate from title
    content = models.TextField()
    summary = models.CharField(
        max_length=150, blank=True, null=True
    )  # eye caching summary of the whole content
    image = models.ImageField(upload_to="post", blank=True, null=True)
    date_posted = models.DateTimeField(timezone.now())
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post-detail", kwargs={"slug": self.slug})

    # # give slug from the title
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     return super(Post, self).save(*args, **kwargs)
