from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("product/<slug:slug>/", views.ViewProduct.as_view(), name="product"),
    path("category/<slug:slug>/", views.ProductCategory.as_view(), name="category"),
    path("brand/<slug:slug>/", views.BrandView.as_view(), name="brand"),
]
