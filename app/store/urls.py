from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("", views.index, name="home"),
    path("contact/", views.FeedbackFormView.as_view(), name="feedback"),
    path("<slug:slug>/", views.PageInfoDetailView.as_view(), name="page_info"),
]
