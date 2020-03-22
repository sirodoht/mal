from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserChangeForm as DjUserChangeForm,
    UserCreationForm as DjUserCreationForm,
)


class UserChangeForm(DjUserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")


class UserCreationForm(DjUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username",)
