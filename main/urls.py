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
    path(
        "documents/<int:document_id>/edit",
        views.document_change,
        name="document_change",
    ),
    path("documents/<int:document_id>/", views.document_read, name="document_read"),
    path("documents/create/", views.document_create, name="document_create"),
]
