from django_filters import rest_framework as filters

from ...models import Product


class ProductFilter(filters.FilterSet):
    """
    Filters the product by the selected attributes.

    Available filters:
        - price: The price of the product, specified as a range.
        - rating: The rating of the product, specified as a range.
        - category: The category of the product, specified as a list of category slugs.
        - brand: The brand of the product, specified as a list of brand slugs.
    """

    price = filters.RangeFilter()
    rating = filters.RangeFilter()
    category = filters.BaseInFilter(field_name="category__name", lookup_expr="in")
    brand = filters.BaseInFilter(field_name="brand__name", lookup_expr="in")

    class Meta:
        model = Product
        fields = [
            "price",
            "rating",
            "category",
            "brand",
        ]
