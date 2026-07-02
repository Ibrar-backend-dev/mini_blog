from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    profile_photo = models.FileField(upload_to="profile_photos/", null=True, blank=True)

    def __str__(self):
        return self.username
    
