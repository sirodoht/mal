from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserChangeForm as DjUserChangeForm,
    UserCreationForm as DjUserCreationForm,
)

from main import models


class UserChangeForm(DjUserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "email"]


class UserCreationForm(DjUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username"]


class DocumentCreationForm(forms.ModelForm):
    class Meta:
        model = models.Document
        fields = ["title", "body"]


class DocumentChangeForm(forms.ModelForm):
    class Meta:
        model = models.Document
        fields = ["title", "body"]
