from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

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


class DocumentDetail(DetailView):
    model = models.Document


class DocumentCreate(SuccessMessageMixin, CreateView):
    model = models.Document
    fields = ["title", "body"]
    success_message = "%(title)s was created successfully"


class DocumentUpdate(SuccessMessageMixin, UpdateView):
    model = models.Document
    fields = ["title", "body"]
    success_message = "%(title)s updated successfully"


class DocumentDelete(DeleteView):
    model = models.Document
    success_url = reverse_lazy("main:index")
