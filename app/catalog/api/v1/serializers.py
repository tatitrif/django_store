from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from ...models import Brand, Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = [
            "created_at",
            "updated_at",
            "is_active",
            "lft",
            "rght",
            "tree_id",
            "level",
        ]
        read_only_fields = ("slug",)


class CategoryProdSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = [
            "created_at",
            "updated_at",
            "is_active",
        ]
        read_only_fields = ("slug",)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = [
            "created_at",
            "updated_at",
            "is_active",
        ]
        read_only_fields = ("slug",)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = [
            "created_at",
            "updated_at",
        ]


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryProdSerializer(
        many=True, queryset=Category.objects.filter(children=None)
    )
    product_image = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        exclude = ["created_at", "updated_at", "is_active", "read_cnt"]
        read_only_fields = ("slug",)
