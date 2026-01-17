from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    username = models.CharField(max_length=255, unique=True)
    avatar_url = models.URLField(max_length=500, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def __str__(self):
        return self.username