from io import BytesIO

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.core.files import File
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from PIL import Image


def get_avator_path(instance, filename):
    """Generate a unique name for the profile image and return its full path."""
    from datetime import date

    ext = filename.split(".")[-1]
    new_filename = f"{instance.user.get_display_name()}_profile_pic.{ext}"
    today_path = date.today().strftime("%Y/%m/%d")
    image_path = f"profile_pics/{today_path}/{new_filename}"
    return image_path


class AccountManager(BaseUserManager):
    """A User manager for a custom user model with no username field used."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extrafields):
        extrafields.setdefault("is_staff", False)
        extrafields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extrafields)

    def create_superuser(self, email, password=None, **extrafields):
        extrafields.setdefault("is_staff", True)
        extrafields.setdefault("is_superuser", True)

        if extrafields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extrafields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self._create_user(email, password, **extrafields)


class Account(AbstractUser):
    """
    A class implementing a fully featured custom User model with
    admin-compliant permissions.

    Email and password are required. Other fields are optional.
    """

    username = None
    email = models.EmailField(
        "email",
        max_length=200,
        unique=True,
        error_messages={
            "unique": "An account with this email address already exists.",
        },
    )
    display_name = models.CharField("display name", max_length=40)

    objects = AccountManager()

    # EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "account"
        verbose_name_plural = "accounts"

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.generate_display_name()
        return super().save(*args, **kwargs)

    def get_display_name(self):
        """Reutrn the best option to display the user's name."""
        if self.first_name and self.last_name:
            return self.get_full_name()
        elif self.first_name:
            return self.get_short_name()
        else:
            return self.display_name

    def generate_display_name(self):
        """Generate a unique diplay name that will be used in urls."""
        display_name = self.email.split("@")[0]
        original_len = len(display_name)
        is_taken = Account.objects.filter(display_name=display_name).exists()

        while is_taken:
            random_str = get_random_string(5, "0123456789")
            if len(display_name) == original_len + 5:
                # A random string is already appended. so remove it
                display_name = display_name[:-5] + random_str
            else:
                display_name += random_str
            is_taken = Account.objects.filter(display_name=display_name).exists()

        return display_name


class Profile(models.Model):
    """Profile of the user besides the information provided during sign up."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.CharField(max_length=150, blank=True)
    about = models.TextField(blank=True)
    avator = models.ImageField(default="default-avator.jpg", upload_to=get_avator_path)
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers", blank=True
    )

    def __str__(self):
        return f"{self.user.display_name}'s profile"

    def save(self, *args, **kwargs):
        img = Image.open(self.avator)
        img = img.convert("RGB")  # for saving the image in JPEG format
        img.thumbnail((150, 150))
        output = BytesIO()
        img.save(output, format="JPEG", quality=80)
        img_file = File(output, name=self.avator.name)
        self.avator = img_file

        super().save(*args, **kwargs)

    @property
    def following_list(self):
        """Return the list of users the user is currently following."""
        following = [profile.user for profile in self.user.profile.following.all()]
        return following

    @property
    def followers_list(self):
        """Return the list of followers of the user."""
        followers = [profile.user for profile in self.user.profile.followers.all()]
        return followers


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_save_profile(sender, instance, created, **kwargs):
    """Automatically create a user profile after sign up OR
    automatically update a user profile when user information is updated.
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
