from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  apodo = models.CharField(max_length=30, default='user1')
    