from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.urls import reverse
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
        upload_to="posts/%Y/%m/%d",
        help_text="Select an eye catching image to be used as a cover photo for your post. "
        "This will attract users to read your post.",
    )
    date_posted = models.DateTimeField(auto_now=True)

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


class Bookmark(models.Model):
    """Bookmark posts for later reading."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookmarks"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.slug


class Comment(models.Model):
    """Users comment on posts."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="", max_length=300)
    date_posted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-date_posted"]
