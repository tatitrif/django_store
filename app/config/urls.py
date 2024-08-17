from config import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("captcha/", include("captcha.urls")),
    path("tinymce/", include("tinymce.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("catalog.api.urls")),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("account/", include("account.urls", namespace="account")),
    path("cart/", include("cart.urls", namespace="cart")),
    path("", include("catalog.urls", namespace="catalog")),
    path("", include("store.urls", namespace="store")),
]

if "debug_toolbar" in settings.INSTALLED_APPS and settings.DEBUG:
    import debug_toolbar

    urlpatterns += (
        [
            path("__debug__/", include(debug_toolbar.urls)),
        ]
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    )

handler404 = "store.views.page_not_found"
handler500 = "store.views.server_error"
handler403 = "store.views.permission_denied"
