from uuid import uuid4
from django.db import models
from django.conf import settings

# Create your models here.

"""

"""
class UserProfile (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    # delete user when user profile is deleted
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile", unique=True)
    bio = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to="users/images")

# end of UserProfile

"""

"""






