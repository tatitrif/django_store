import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = [
        "product",
    ]


@admin.action(description=_("Export to CSV"))
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename={}.csv".format(opts)
    writer = csv.writer(response)

    fields = [
        field
        for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    # write the header row
    writer.writerow([field.verbose_name for field in fields])
    # write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%d/%m/%Y")
            data_row.append(value)
        writer.writerow(data_row)
    return response


@admin.display(description=_("Order"))
def order_detail(obj):
    url = reverse("order:admin_order_detail", args=[obj.id])
    text = _("View")
    return format_html(f'<a href="{url}">{text}</a>')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = [
        "is_paid",
    ]
    inlines = [OrderItemInline]
    actions = [export_to_csv]
    list_display = (
        "id",
        "get_total_cost",
        order_detail,
    )

    @admin.display(description=_("Total"), ordering="is_paid")
    def get_total_cost(self, o: Order):
        return sum(item.get_cost() for item in o.items.all())
