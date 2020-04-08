from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView

from main import forms, models


class Index(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super(Index, self).get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            context["docs"] = models.Document.objects.filter(owner=self.request.user)
        return context


class UserDetail(DetailView):
    model = models.User


class UserCreate(SuccessMessageMixin, CreateView):
    form_class = forms.UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "main/user_create.html"
    success_message = "Welcome!"


class UserUpdate(SuccessMessageMixin, UpdateView):
    model = models.User
    fields = ["username", "email"]
    success_message = "%(username)s updated successfully"
    template_name = "main/user_update.html"


class UserDelete(DeleteView):
    model = models.User
    success_url = reverse_lazy("index")


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
    success_url = reverse_lazy("index")


class FileFieldView(FormView):
    form_class = forms.UploadFilesForm
    template_name = "main/document_import.html"
    success_url = reverse_lazy("index")

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


@login_required
def document_purge(request):
    if request.method == "POST":
        models.Document.objects.filter(owner=request.user).delete()
        return redirect("index")
    else:
        return render(request, "main/document_purge_confirm_delete.html")
