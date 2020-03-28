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

urlpatterns += [
    path("documents/<int:pk>/", views.DocumentDetail.as_view(), name="document_detail"),
    path("documents/create/", views.DocumentCreate.as_view(), name="document_create"),
    path(
        "documents/<int:pk>/edit/",
        views.DocumentUpdate.as_view(),
        name="document_update",
    ),
    path(
        "documents/<int:pk>/delete/",
        views.DocumentDelete.as_view(),
        name="document_delete",
    ),
]
