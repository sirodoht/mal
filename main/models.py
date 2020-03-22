from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


class Document(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
