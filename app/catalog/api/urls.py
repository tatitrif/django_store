from django.urls import include, path

urlpatterns = (path("v1/", include("catalog.api.v1.urls")),)
