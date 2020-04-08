from django.contrib import admin
from django.urls import include, path

from main import views

admin.site.site_header = "mal administration"

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/create/", views.UserCreate.as_view(), name="user_create"),
    path("accounts/<int:pk>/", views.UserDetail.as_view(), name="user_detail"),
    path("accounts/<int:pk>/edit/", views.UserUpdate.as_view(), name="user_update"),
    path("accounts/<int:pk>/delete/", views.UserDelete.as_view(), name="user_delete"),
    path("accounts/<int:user_id>/cleanup/", views.user_cleanup, name="user_cleanup"),
    path("import/", views.FileFieldView.as_view(), name="import_md"),
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
