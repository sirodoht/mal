from main import models


def sidebar(request):
    return {
        "documents": models.Document.objects.all().order_by("title"),
        "featured": models.Document.objects.filter(is_featured=True),
    }
