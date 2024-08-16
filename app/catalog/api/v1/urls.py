from django.urls import path

from .views import (
    BrandDetailApi,
    BrandListApi,
    CategoryDetailApi,
    CategoryListApi,
    ProductDetailApi,
    ProductImageDetailApi,
    ProductImageListApi,
    ProductListApi,
)

urlpatterns = [
    path("product/", ProductListApi.as_view()),
    path("product/<uuid:pk>", ProductDetailApi.as_view()),
    path("brand/<uuid:pk>", BrandDetailApi.as_view()),
    path("brand/", BrandListApi.as_view()),
    path("product/image/<uuid:pk>", ProductImageDetailApi.as_view()),
    path("product/image/", ProductImageListApi.as_view()),
    path("category/", CategoryListApi.as_view()),
    path("category/<uuid:pk>", CategoryDetailApi.as_view()),
]
