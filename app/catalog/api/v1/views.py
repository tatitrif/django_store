from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser

from ...models import Brand, Category, Product, ProductImage
from .filters import ProductFilter
from .serializers import (
    BrandSerializer,
    CategorySerializer,
    ProductImageSerializer,
    ProductSerializer,
)


class ProductListApi(generics.ListCreateAPIView):
    """
    Fetch list of all product and create product here
    """

    queryset = (
        Product.active_obj.prefetch_related("product_image", "category")
        .select_related(
            "brand",
        )
        .order_by("name")
    )
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = [
        "name",
    ]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [
                AllowAny,
            ]
        else:
            self.permission_classes = [
                IsAdminUser,
            ]
        return super().get_permissions()


class ProductDetailApi(RetrieveUpdateDestroyAPIView):
    """
    Allows AdminUsers to retrieve, update, or delete data for a Product.
    """

    queryset = Product.active_obj.order_by("name")
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [
                AllowAny,
            ]
        else:
            self.permission_classes = [
                IsAdminUser,
            ]
        return super().get_permissions()


class BrandListApi(ListAPIView):
    """
    Fetch list of all Brands and create new Brand.
    """

    queryset = Brand.active_obj.all()
    serializer_class = BrandSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [
                AllowAny,
            ]
        else:
            self.permission_classes = [
                IsAdminUser,
            ]
        return super().get_permissions()


class BrandDetailApi(RetrieveUpdateDestroyAPIView):
    """
    Allows AdminUsers to retrieve, update, or delete data for a Brand.
    """

    queryset = Brand.active_obj.all()
    serializer_class = BrandSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [
                AllowAny,
            ]
        else:
            self.permission_classes = [
                IsAdminUser,
            ]
        return super().get_permissions()


class CategoryListApi(generics.ListCreateAPIView):
    """
    Fetch list of all Categories and create new Category.
    """

    queryset = Category.active_obj.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [
                AllowAny,
            ]
        else:
            self.permission_classes = [
                IsAdminUser,
            ]
        return super().get_permissions()


class CategoryDetailApi(RetrieveUpdateDestroyAPIView):
    """
    Allows AdminUsers to retrieve, update, or delete data for a Category.
    """

    queryset = Category.active_obj.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [
                AllowAny,
            ]
        else:
            self.permission_classes = [
                IsAdminUser,
            ]
        return super().get_permissions()


class ProductImageListApi(generics.ListCreateAPIView):
    """
    Fetch list of all product Image and create new Product Image.
    """

    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [
                AllowAny,
            ]
        else:
            self.permission_classes = [
                IsAdminUser,
            ]
        return super().get_permissions()


class ProductImageDetailApi(RetrieveUpdateDestroyAPIView):
    """
    Allows AdminUsers to retrieve, update, or delete data for a Product Image.
    """

    parser_classes = (MultiPartParser, FormParser)
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [
                AllowAny,
            ]
        else:
            self.permission_classes = [
                IsAdminUser,
            ]
        return super().get_permissions()
