from django.urls import path

from . import views

app_name = "order"

urlpatterns = [
    path(
        "admin/order/<uuid:order_id>/",
        views.admin_order_detail,
        name="admin_order_detail",
    ),
]
