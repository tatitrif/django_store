from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView

from .forms import FeedbackForm
from .models import PageInfo


class DataMixin:
    name = None
    extra_context = {}

    def __init__(self):
        if self.name:
            self.extra_context["title"] = self.name

    def get_mixin_context(self, context, **kwargs):
        context.update(kwargs)
        return context


def index(request) -> HttpResponse:
    extra_context = {"title_section": True}
    return render(request, "store/index.html", context=extra_context)


class PageInfoDetailView(DataMixin, DetailView):
    """
    Renders pages used for site descriptive pages
    """

    template_name = "store/detail.html"
    context_object_name = "item"
    extra_context = {"breadcrumbs": True}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        return self.get_mixin_context(
            context,
            title=page.name,
            meta_title=page.meta_title,
            meta_description=page.meta_description,
            title_page=page.name,
            page=page,
        )

    def get_object(self, queryset=None):
        return get_object_or_404(
            PageInfo.active_obj, slug=self.kwargs[self.slug_url_kwarg]
        )


class FeedbackFormView(CreateView):
    """
    Renders contact Form.
    """

    form_class = FeedbackForm
    template_name = "store/contact.html"
    success_url = reverse_lazy("store:home")
    extra_context = {
        "button_text": _("Submit"),
        "breadcrumbs": True,
        "title_section": True,
    }

    def form_valid(self, form):
        form.save(commit=False)
        return super().form_valid(form)


def page_not_found(request, exception, template_name="store/errors/404.html"):
    return render(
        request,
        template_name,
        {
            "path": request.path,
        },
        HTTPStatus.NOT_FOUND,
    )


def server_error(request):
    return render(request, "store/errors/500.html", HTTPStatus.INTERNAL_SERVER_ERROR)


def permission_denied(request, exception):
    return render(request, "store/errors/403.html", HTTPStatus.FORBIDDEN)
