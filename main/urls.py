from django.contrib import admin
from django.urls import include, path

from main import views

admin.site.site_header = "mal administration"
app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/profile/", views.profile, name="profile"),
    path("accounts/create/", views.signup, name="signup"),
]
