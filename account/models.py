from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from PIL import Image


class CustomUserManger(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    """
    A class implementing a fully featured custom User model with
    admin-compliant permissions.

    Email and password are required. Other fields are optional.
    """

    email = models.EmailField("email", max_length=200, unique=True)
    first_name = models.CharField("first name", max_length=40, blank=True)
    last_name = models.CharField("last name", max_length=40, blank=True)
    display_name = models.CharField(
        "display name", max_length=40, blank=True, null=True
    )
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text="Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts.",
    )
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField("date joined", auto_now_add=True)

    objects = CustomUserManger()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "account"
        verbose_name_plural = "accounts"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def save(self, *args, **kwargs):
        self.display_name = self.get_display_name()
        return super().save(*args, **kwargs)

    def get_display_name(self):
        """Set display name when the user signed up."""
        if self.display_name:
            return
        if self.first_name and self.last_name:
            display_name = self.get_full_name()
        elif self.first_name:
            display_name = self.get_short_name()
        else:
            # the username part of the email address
            display_name = "@" + self.email.split("@")[0]
        return display_name


class Profile(models.Model):
    """Profile of the user besides the information provided during sign up."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.CharField(max_length=150, blank=True)
    about = models.TextField(blank=True)
    profile_picture = models.ImageField(
        default="default-profile-pic.jpg", upload_to="profile_pics"
    )

    def __str__(self):
        return f"{self.user.display_name} profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_picture.path)
        if img.width > 300 or img.height > 300:
            img.thumbnail(size=(300, 300))
            img.save(self.profile_picture.path)  # replace the larger image

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_or_save_profile(sender, instance, created, **kwargs):
        """Automatically create user profile after sign up OR
        Automatically update user profile when user information is updated.
        """
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()
