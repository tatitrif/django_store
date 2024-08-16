from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser, PermissionsMixin):
    objects = CustomUserManager()
    image = models.ImageField(
        upload_to="account/",
        verbose_name=_("image"),
        null=True,
        blank=True,
    )
    date_birth = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Birthday"),
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        _("created_at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("updated_at"),
        auto_now=True,
    )

    def __str__(self):
        return self.username
