from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import FeedbackForm
from .models import PageInfo


def index(request) -> HttpResponse:
    return render(request, "store/index.html")


class PageInfoDetailView(DetailView):
    """
    Finds the object associated with the current HTTP request and displays the object details in a template
    """

    template_name = "store/detail.html"
    context_object_name = "item"

    def get_object(self, queryset=None) -> object:
        return get_object_or_404(
            PageInfo.active_obj, slug=self.kwargs[self.slug_url_kwarg]
        )


class FeedbackFormView(CreateView):
    """
    Renders contact form.
    """

    form_class = FeedbackForm
    template_name = "store/contact.html"
    success_url = reverse_lazy("store:home")

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
