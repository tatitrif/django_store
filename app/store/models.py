import uuid

from config.settings import SCHEME_DB
from django.contrib.sites.models import Site
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField


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


class ContactInfo(BaseModel):
    site = models.OneToOneField(
        Site, on_delete=models.CASCADE, default=1, related_name="site"
    )
    name = models.CharField(
        verbose_name=_("Name"),
        blank=True,
        default=None,
        max_length=150,
        validators=[
            MaxLengthValidator(150),
        ],
    )
    address = models.CharField(
        verbose_name=_("Address"),
        blank=True,
        default=None,
        max_length=150,
        validators=[
            MaxLengthValidator(150),
        ],
    )
    email = models.EmailField(
        verbose_name=_("Email"),
        blank=True,
        default=None,
        max_length=150,
        validators=[
            MaxLengthValidator(150),
        ],
    )
    phone = models.CharField(
        verbose_name=_("Phone"),
        blank=True,
        default=None,
        max_length=150,
        validators=[
            MaxLengthValidator(150),
        ],
    )

    class Meta:
        db_table = f"{SCHEME_DB}contact_info"
        verbose_name = _("Store contact info")
        verbose_name_plural = _("Stores contact info")

    def __str__(self):
        return self.site.name


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class TopMenuManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(top_menu=True, is_active=True)


class BottomMenuManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(bottom_menu=True, is_active=True)


class PageInfo(BaseModel):
    objects = models.Manager()
    active_obj = PublishedManager()
    top_menu_obj = TopMenuManager()
    bottom_menu_obj = BottomMenuManager()

    site = models.ForeignKey(Site, on_delete=models.CASCADE, default=1)
    name = models.CharField(
        unique=True,
        verbose_name=_("Name"),
        max_length=150,
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(150),
        ],
    )
    body = HTMLField(
        verbose_name=_("Body"),
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        verbose_name=_("Slug"),
        max_length=150,
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(150),
        ],
    )
    meta_title = models.CharField(
        verbose_name=_("Meta title"),
        null=True,
        blank=True,
        max_length=250,
    )
    meta_description = models.CharField(
        verbose_name=_("Meta description"),
        null=True,
        blank=True,
        max_length=250,
    )
    is_active = models.BooleanField(
        verbose_name=_("Visibility"),
        default=True,
    )
    top_menu = models.BooleanField(
        verbose_name=_("Add to top menu"),
        default=True,
    )
    bottom_menu = models.BooleanField(
        verbose_name=_("Add to bottom menu"),
        default=True,
    )

    class Meta:
        db_table = f"{SCHEME_DB}page_info"
        verbose_name = _("Page Info")
        verbose_name_plural = _("Pages Info")

    def __str__(self):
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("store:page_info", kwargs={"slug": self.slug})


class Feedback(BaseModel):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=150,
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(150),
        ],
    )
    email = models.EmailField(
        verbose_name=_("Email"),
        max_length=150,
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(150),
        ],
    )
    msg = models.CharField(
        verbose_name=_("message"),
        max_length=150,
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(150),
        ],
    )
    captcha = models.CharField(
        verbose_name=_("Captcha"),
        max_length=150,
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(150),
        ],
    )

    class Meta:
        db_table = f"{SCHEME_DB}feedback"
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedbacks")

    def __str__(self):
        return self.email
