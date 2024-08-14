from django.contrib import admin

from .models import Feedback, PageInfo, StoreInfo


@admin.register(PageInfo)
class PageInfoAdmin(admin.ModelAdmin):
    exclude = [
        "is_active",
    ]
    readonly_fields = [
        "updated_at",
        "created_at",
    ]
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        "name",
        "updated_at",
        "created_at",
    )
    list_display_links = ("name",)
    ordering = [
        "-updated_at",
        "name",
    ]
    search_fields = [
        "name",
    ]
    save_on_top = True
    save_as = True


@admin.register(StoreInfo)
class StoreInfoAdmin(admin.ModelAdmin):
    list_display = (
        "site",
        "address",
        "email",
        "phone",
        "updated_at",
        "created_at",
    )
    readonly_fields = [
        "updated_at",
        "created_at",
    ]
    ordering = [
        "-updated_at",
    ]
    save_on_top = True
    save_as = True


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "msg",
        "captcha",
        "updated_at",
        "created_at",
    )
    readonly_fields = [
        "updated_at",
        "created_at",
        "captcha",
    ]
    ordering = [
        "-created_at",
    ]
    save_on_top = True
    save_as = True
