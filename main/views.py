from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView

from main import forms, models


def index(request):
    return render(request, "main/index.html")


class UserDetail(DetailView):
    model = models.User


class UserCreate(SuccessMessageMixin, CreateView):
    form_class = forms.UserCreationForm
    success_url = reverse_lazy("main:login")
    template_name = "main/user_create.html"
    success_message = "Welcome!"


class UserUpdate(SuccessMessageMixin, UpdateView):
    model = models.User
    fields = ["username", "email"]
    success_message = "%(username)s updated successfully"
    template_name = "main/user_update.html"


class UserDelete(DeleteView):
    model = models.User
    success_url = reverse_lazy("main:index")


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


class FileFieldView(FormView):
    form_class = forms.UploadFilesForm
    template_name = "main/import_md.html"
    success_url = reverse_lazy("main:index")

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist("file")
        if form.is_valid():
            for f in files:
                content = f.read().decode("utf-8")
                models.Document.objects.create(
                    title=f.name, body=content, owner=request.user
                )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
