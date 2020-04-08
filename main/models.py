import markdown
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    about = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.username


class Document(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_featured = models.BooleanField(default=False)

    @property
    def as_markdown(self):
        return markdown.markdown(
            self.body,
            extensions=[
                "markdown.extensions.fenced_code",
                "markdown.extensions.tables",
            ],
        )

    def get_absolute_url(self):
        return reverse("document_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title
