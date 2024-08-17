from cart.forms import CartAddProductForm
from config.settings import PAGINATE_BY
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Brand, Category, Product


class DataMixin:
    paginate_by = PAGINATE_BY
    extra_context = {"breadcrumbs": True, "title_section": True}

    def get_mixin_context(self, context, **kwargs):
        context.update(kwargs)
        return context


class ViewProduct(DetailView):
    """
    View for displaying the detailed page of a product card.
    """

    template_name = "catalog/product.html"
    slug_url_kwarg = "slug"
    context_object_name = "context"
    extra_context = {
        "breadcrumbs": True,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        product.read_cnt += 1
        product.save()
        context["title"] = product.name
        context["meta_keywords"] = product.meta_keywords
        context["meta_description"] = product.meta_description
        context["product"] = product
        context["cart_product_form"] = CartAddProductForm

        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Product.objects, slug=self.kwargs[self.slug_url_kwarg])


class ProductCategory(DataMixin, ListView):
    """
    View for displaying  products by category.
    """

    template_name = "catalog/product_category.html"
    context_object_name = "products"
    # allow_empty = False

    def get_queryset(self):
        self.cat = Category.active_obj.get(slug=self.kwargs["slug"])
        categories = self.cat.get_descendants(include_self=True)
        products = (
            Product.active_obj.filter(category__in=categories)
            .prefetch_related("category")
            .order_by("name")
        )
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title=self.cat.name,
            meta_keywords=self.cat.meta_keywords if self.cat.meta_keywords else "",
            meta_description=(
                self.cat.meta_description if self.cat.meta_description else ""
            ),
            title_page=self.cat.name,
            title_image_url=self.cat.image.url if self.cat.image else "",
            title_description=self.cat.description if self.cat.description else "",
            category=self.cat,
        )


class BrandView(DataMixin, ListView):
    """
    View for displaying products by brand.
    """

    template_name = "catalog/product_brand.html"
    context_object_name = "products"
    allow_empty = False

    def get_queryset(self):
        self.brand = Brand.active_obj.get(slug=self.kwargs["slug"])
        products = Product.active_obj.filter(brand=self.brand).select_related("brand")
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.brand.name
        context["brand"] = self.brand
        return self.get_mixin_context(
            context,
            meta_keywords=self.brand.meta_keywords if self.brand.meta_keywords else "",
            meta_description=(
                self.brand.meta_description if self.brand.meta_description else ""
            ),
            title_page=self.brand.name,
            title_description=self.brand.description if self.brand.description else "",
        )
