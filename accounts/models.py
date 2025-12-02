from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank = True, max_length = 300)
    profile_pic = models.ImageField(upload_to = 'profiles/', blank = True, null = True)
    is_verified = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.username
