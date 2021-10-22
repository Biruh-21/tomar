from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.base import ModelBase
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    """Category of posts written for ease of reading."""

    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Post(models.Model):
    """Posts written by users or admin."""

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)  # automatically generate from title
    content = RichTextUploadingField()
    image = models.ImageField(
        upload_to="posts/%Y/%m/%d", blank=True
    )  # have a default image incase the user don't provide and image
    date_posted = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    bookmark = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="bookmark", blank=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post-detail", kwargs={"slug": self.slug})

    # give slug from the title
    def save(self, *args, **kwargs):
        self.slug = self.unique_slug_generator(self.title)
        return super().save(*args, **kwargs)

    def unique_slug_generator(self, title):
        """Generate unique slug from the post title."""
        unique_slug = slugify(title)  # convert the post title to slug
        # is there any post with this slug
        slug_is_taken = Post.objects.filter(slug=unique_slug).exists()

        while slug_is_taken:
            random_string = get_random_string(length=12)
            unique_slug += "-" + random_string
            slug_is_taken = Post.objects.filter(slug=unique_slug).exists()

        return unique_slug
