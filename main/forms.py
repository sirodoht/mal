from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as DjUserCreationForm

from main import models


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


class UploadFilesForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": True}))
