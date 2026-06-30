from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.address.models import Address
class User(AbstractUser):
    
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='users', null=True, blank=True)
    profile_photo=models.FileField(upload_to="profile_photos/" , null= True , blank= True)

    def __str__(self):
        return self.username
    
