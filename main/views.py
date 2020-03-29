from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from main import forms, models


def index(request):
    return render(request, "main/index.html")


class UserDetail(DetailView):
    model = models.User


class UserCreate(CreateView):
    form_class = forms.UserCreationForm
    success_url = reverse_lazy("main:login")
    template_name = "main/user_create.html"


class DocumentDetail(DetailView):
    model = models.Document


class DocumentCreate(SuccessMessageMixin, CreateView):
    model = models.Document
    fields = ["title", "body"]
    success_message = "%(title)s was created successfully"


class DocumentUpdate(SuccessMessageMixin, UpdateView):
    model = models.Document
    fields = ["title", "body", "is_featured"]
    success_message = "%(title)s updated successfully"


class DocumentDelete(DeleteView):
    model = models.Document
    success_url = reverse_lazy("main:index")
