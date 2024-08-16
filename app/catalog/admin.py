from django import forms
from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple, FileInput, ImageField, NumberInput
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from mptt.admin import DraggableMPTTAdmin
from mptt.models import TreeManyToManyField

from .models import Brand, Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


class FilterCategories(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(children=None)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ("category",)
    readonly_fields = (
        "created_at",
        "read_cnt",
        "product_img",
    )
    save_as = True
    save_on_top = True
    inlines = (ProductImageInline,)
    list_display = (
        "name",
        "product_img",
        "price",
        "rating",
    )
    list_editable = ("price",)
    prepopulated_fields = {
        "slug": ("name",),
    }
    form = FilterCategories
    formfield_overrides = {
        TreeManyToManyField: {"widget": CheckboxSelectMultiple},
        models.FloatField: {
            "widget": NumberInput(
                attrs={"style": "width: 4em;", "min": 0, "max": 10, "step": 0.1}
            )
        },
    }

    @admin.display(description=_("Image"), ordering="name")
    def product_img(self, p: Product):
        if p.get_image():
            return format_html(f"<img src='{p.get_image()}' width=50>")
        return _("no image")


@admin.register(Category)
class CustomMPTTModelAdmin(DraggableMPTTAdmin):
    formfield_overrides = {
        ImageField: {"widget": FileInput},
    }
    save_as = True
    save_on_top = True
    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    exclude = ("is_active",)
    save_as = True
    save_on_top = True
    prepopulated_fields = {
        "slug": ("name",),
    }
