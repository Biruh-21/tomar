from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save


class Profile(models.Model):
    """Profile of the user besides the information provided during sign up."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=150, blank=True)
    about = models.TextField(blank=True)
    profile_picture = models.ImageField(
        default="default-profile-pic.jpg", upload_to="profile_pics"
    )

    def __str__(self):
        return f"{self.user.username} profile"

    @receiver(post_save, sender=User)
    def create_or_save_profile(sender, instance, created, **kwargs):
        """Automatically create user profile after sign up OR
        Automatically update user profile when user information is updated.
        """
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()
