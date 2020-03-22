from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main import models


class Admin(UserAdmin):
    list_display = ("id", "username", "email", "date_joined", "last_login")


admin.site.register(models.User, Admin)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


admin.site.register(models.Document, DocumentAdmin)
