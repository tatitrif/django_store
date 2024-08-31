import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


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


class Order(BaseModel):
    first_name = models.CharField(
        max_length=50,
        verbose_name=_("First Name"),
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name=_("Last Name"),
    )
    email = models.EmailField(
        verbose_name=_("E-mail"),
    )
    address = models.CharField(
        max_length=250,
        verbose_name=_("Address"),
    )
    postal_code = models.CharField(
        max_length=20,
        verbose_name=_("Postal Code"),
    )
    city = models.CharField(
        max_length=100,
        verbose_name=_("City"),
    )
    is_paid = models.BooleanField(
        default=False,
        verbose_name=_("Paid"),
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        "catalog.Product", related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Price"),
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Qty"),
    )

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
