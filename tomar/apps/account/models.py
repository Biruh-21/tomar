from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Profile of the user besides the information provided during sign up."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=150)
    about = models.TextField()
    profile_picture = models.ImageField(
        default="default-profile-pic.jpg", upload_to="profile_pics"
    )

    def __str__(self):
        return f"{self.user.username} profile"
