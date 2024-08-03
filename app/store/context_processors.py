from config import settings

from .models import ContactInfo, PageInfo

store = ContactInfo.objects.filter(site_id=settings.SITE_ID)
store_exists = ContactInfo.objects.filter(site_id=settings.SITE_ID).exists()
top_menu = PageInfo.top_menu_obj.filter(site_id=settings.SITE_ID)
top_menu_exists = PageInfo.top_menu_obj.filter(site_id=settings.SITE_ID).exists()
bottom_menu = PageInfo.bottom_menu_obj.filter(site_id=settings.SITE_ID)
bottom_menu_exists = PageInfo.bottom_menu_obj.filter(site_id=settings.SITE_ID).exists()
lang = settings.LANGUAGE_CODE


def get_store_context(request):
    return dict(
        lang=lang,
        store=store if store_exists else list(),
        store_name=store.first().name if store_exists else "",
        top_menu=top_menu if top_menu_exists else list(),
        bottom_menu=bottom_menu if bottom_menu_exists else list(),
    )
