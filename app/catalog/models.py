import logging
import uuid

from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManager, TreeManyToManyField
from pytils import translit
from tinymce.models import HTMLField

logger = logging.getLogger(__name__)


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(
        _("created_at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("updated_at"),
        auto_now=True,
    )

    class Meta:
        abstract = True


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class DescribeModel(models.Model):
    objects = models.Manager()
    active_obj = PublishedManager()

    name = models.CharField(
        unique=True,
        verbose_name=_("Title"),
        max_length=50,
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(50),
        ],
    )
    description = HTMLField(
        verbose_name=_("Short description"),
        null=True,
        blank=True,
        validators=[MaxLengthValidator(1000)],
    )
    meta_description = models.CharField(
        verbose_name=_("Meta description"),
        null=True,
        blank=True,
        max_length=50,
        validators=[
            MaxLengthValidator(50),
        ],
    )
    meta_keywords = models.CharField(
        verbose_name=_("Meta keywords"),
        null=True,
        blank=True,
        max_length=50,
        validators=[
            MaxLengthValidator(50),
        ],
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        verbose_name=_("slug"),
        max_length=50,
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(50),
        ],
    )
    is_active = models.BooleanField(
        verbose_name=_("visibility"),
        default=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = translit.slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        abstract = True


class Brand(BaseModel, DescribeModel):
    class Meta:
        ordering = ["name"]
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def get_absolute_url(self) -> str:
        return reverse("catalog:brand", kwargs={"slug": self.slug})


class Category(MPTTModel, BaseModel, DescribeModel):
    objects = models.Manager()
    tree_objects = TreeManager()
    """
    Category Table implemented with MPTT.
    """
    image = models.ImageField(
        upload_to="catalog/category/",
        verbose_name=_("image"),
        null=True,
        blank=True,
        help_text=_("Upload a category image"),
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name=_("Parent Category"),
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self) -> str:
        return reverse("catalog:category", kwargs={"slug": self.slug})

    def get_product_count(self) -> int:
        """
        Gets the number of products in this category and its nested subcategories.

        :return: The number of products in this category and its nested subcategories.
        """
        list_categories = self.get_descendants(include_self=True)
        return Product.objects.filter(category__in=list_categories).distinct().count()

    def get_product(self) -> int:
        """
        Gets the number of products in this category and its nested subcategories.

        :return: The number of products in this category and its nested subcategories.
        """
        list_categories = self.get_descendants(include_self=True)
        return Product.objects.filter(category__in=list_categories).distinct()

    def get_full_name(self):
        names = self.get_ancestors(include_self=True).values("name")
        full_name = " - ".join(map(lambda x: x["name"], names))
        return full_name

    @staticmethod
    def get_all_categories() -> QuerySet:
        """
        Gets all categories in the database.

        :return: A QuerySet containing all categories in the database.
        """
        try:
            return Category.objects.all()
        except Category.DoesNotExist as error:
            logger.error(f"No found categories: {error}")
            return Category.objects.none()


class Product(BaseModel, DescribeModel):
    """
    Product table
    """

    brand = models.ForeignKey(
        Brand, blank=True, null=True, related_name="brand", on_delete=models.CASCADE
    )
    category = TreeManyToManyField(
        Category,
        related_name="products",
        verbose_name=_("category"),
    )
    long_descr = HTMLField(
        verbose_name=_("Long description"),
        blank=True,
        null=True,
    )
    price = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_("price"),
    )

    rating = models.FloatField(
        verbose_name=_("rating"),
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        default=0,
    )

    read_cnt = models.IntegerField(blank=True, null=True, default=0)

    def get_absolute_url(self) -> str:
        return reverse("catalog:product", kwargs={"slug": self.slug})

    def get_image_set(self):
        if self.product_image:
            return self.product_image.all()

    def get_image(self):
        if self.product_image:
            return self.product_image.last()
        return self.product_image

    def get_category(self):
        """
        Gets the product in this category and its nested subcategories.

        :return: The  category and its ancestors categories.
        """
        return Category.tree_objects.get_queryset_ancestors(
            self.category, include_self=True
        )


def model_file_upload_to(instance, filename):
    ext = filename.split(".")
    file_name = hash(ext[0])
    file_extension = ext[-1]
    return f"catalog/products/{instance.product.id}/{file_name}.{file_extension}"


class ProductImage(BaseModel):
    """
    The product image table.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        related_name="product_image",
    )
    image = models.ImageField(
        upload_to=model_file_upload_to,
        verbose_name=_("image"),
        help_text=_("Upload a product image"),
    )

    alt_text = models.CharField(
        verbose_name=_("Alternative text"),
        help_text=_("Please add alternative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    rank = models.PositiveSmallIntegerField(
        verbose_name=_("Position"),
        help_text=_("Smallest will be last"),
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        default=0,
    )

    def __str__(self):
        return self.image.url

    class Meta:
        ordering = ["-rank"]
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
