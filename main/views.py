import io
import uuid
import zipfile

from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView

from main import forms, models


class Index(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super(Index, self).get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            context["docs"] = models.Document.objects.filter(
                owner=self.request.user
            ).order_by("-updated_at")
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


class DocumentFeaturize(UpdateView):
    model = models.Document
    fields = ["is_featured"]


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


def document_export(request):
    # get all documents and add them into export_data encoded
    documents = models.Document.objects.all()
    export_data = []
    for doc in documents:
        title = doc.title.replace(":", "--") + ".md"
        export_data.append((title, io.BytesIO(doc.body.encode())))

    # create zip archive in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_name, data in export_data:
            zip_file.writestr(file_name, data.getvalue())

    cropped_uuid = str(uuid.uuid4())[:8]
    response = HttpResponse(zip_buffer.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = f"attachment; filename=export-{cropped_uuid}.zip"
    return response


class APIDocumentList(ListView):
    model = models.Document

    def render_to_response(self, context):
        queryset = self.model.objects.all()
        data = serializers.serialize("json", queryset, fields=("title", "body"))
        return HttpResponse(data, content_type="application/json")
