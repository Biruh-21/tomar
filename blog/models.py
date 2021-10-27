import os
from io import BytesIO

from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.core.files import File
from django.dispatch import receiver
from PIL import Image, ImageOps
from ckeditor.fields import RichTextField


def get_image_path(instance, filename):
    """Generate a unique name for the image and return its full path."""
    from datetime import date

    ext = filename.split(".")[-1]
    new_filename = f"{instance.slug}.{ext}"
    today_path = date.today().strftime("%Y/%m/%d")
    image_path = f"posts/{today_path}/{new_filename}"
    return image_path


class Category(models.Model):
    """Category of posts written for ease of reading."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    """Posts written by users or admin."""

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)  # automatically generate from title
    content = RichTextField()
    image = models.ImageField(
        upload_to=get_image_path,
        help_text="Select an eye catching image to be used as a cover photo for your post. "
        "This will attract users to read your post.",
    )
    date_posted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        img = Image.open(self.image)
        img = img.convert("RGB")  # for saving the image in JPEG format
        img = ImageOps.exif_transpose(img)
        img = ImageOps.fit(img, (1200, 630))  # resing and croping the image
        output = BytesIO()
        img.save(output, format="JPEG", quality=80)
        img_file = File(output, name=self.image.name)
        self.image = img_file
        # assign a unique slug from the title of the post
        self.slug = unique_slug_generator(self.title)

        super().save(*args, **kwargs)


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


def unique_slug_generator(title):
    """Generate unique slug from the post title."""
    unique_slug = slugify(title)  # convert the post title to slug
    # is there any post with this slug
    slug_is_taken = Post.objects.filter(slug=unique_slug).exists()

    while slug_is_taken:
        random_string = get_random_string(length=12)
        unique_slug += "-" + random_string
        slug_is_taken = Post.objects.filter(slug=unique_slug).exists()

    return unique_slug


@receiver(post_delete, sender=Post)
def post_delete_image_handler(sender, instance, *args, **kwargs):
    """Deletes the image associated with the post after the post has been deleted."""
    if instance.image and instance.image.url:
        try:
            os.remove(instance.image.path)
        except OSError:
            # if the image doesn't exist, pass it
            pass
