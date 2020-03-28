from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from main import forms, models


def index(request):
    return render(
        request,
        "main/index.html",
        {
            "documents": models.Document.objects.all(),
            "featured": models.Document.objects.filter(is_featured=True),
        },
    )


@login_required
def profile(request):
    return render(
        request,
        "main/profile.html",
        {
            "documents": models.Document.objects.all(),
            "featured": models.Document.objects.filter(is_featured=True),
        },
    )


def signup(request):
    if request.user.is_authenticated:
        return redirect("main:profile")

    if request.method == "POST":
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("main:login")
    else:
        form = forms.UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def document_read(request, document_id):
    doc = models.Document.objects.get(id=document_id)
    return render(
        request,
        "main/document_read.html",
        {
            "documents": models.Document.objects.all(),
            "featured": models.Document.objects.filter(is_featured=True),
            "doc": doc,
        },
    )


def document_create(request):
    if request.method == "POST":
        form = forms.DocumentCreationForm(request.POST)
        if form.is_valid():
            doc = form.save()
            return redirect("main:document_read", doc.id)
    else:
        form = forms.DocumentCreationForm()
    return render(
        request,
        "main/document_create.html",
        {
            "documents": models.Document.objects.all(),
            "featured": models.Document.objects.filter(is_featured=True),
            "form": form,
        },
    )


def document_change(request, document_id):
    doc = models.Document.objects.get(id=document_id)
    if request.method == "POST":
        form = forms.DocumentChangeForm(request.POST, instance=doc)
        if form.is_valid():
            doc = form.save()
            messages.success(request, "Document saved")
            return redirect("main:document_read", doc.id)
    else:
        form = forms.DocumentChangeForm(instance=doc)
    return render(
        request,
        "main/document_change.html",
        {
            "documents": models.Document.objects.all(),
            "featured": models.Document.objects.filter(is_featured=True),
            "form": form,
        },
    )
