# Generated by Django 3.0.4 on 2020-03-24 00:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_document_is_pinned"),
    ]

    operations = [
        migrations.RenameField(
            model_name="document", old_name="is_pinned", new_name="is_featured",
        ),
    ]
