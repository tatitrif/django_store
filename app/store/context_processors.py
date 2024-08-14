from config import settings

from .models import PageInfo, StoreInfo

store = StoreInfo.objects.filter(site_id=settings.SITE_ID)
store_exists = store.exists()

top_menu = PageInfo.top_menu_obj.filter(site_id=settings.SITE_ID)
top_menu_exists = PageInfo.top_menu_obj.filter(site_id=settings.SITE_ID).exists()
bottom_menu = PageInfo.bottom_menu_obj.filter(site_id=settings.SITE_ID)
bottom_menu_exists = PageInfo.bottom_menu_obj.filter(site_id=settings.SITE_ID).exists()
lang = settings.LANGUAGE_CODE


def get_store_context(request):
    return dict(
        lang=lang,
        store_info=store if store_exists else list(),
        store_name=store.first().name if store_exists else "",
        top_menu=top_menu if top_menu_exists else list(),
        bottom_menu=bottom_menu if bottom_menu_exists else list(),
        store_description=store.first().description if store_exists else "",
        meta_description=store.first().meta_description if store_exists else "",
        meta_keywords=store.first().meta_keywords if store_exists else "",
        title=store.first().title if store_exists else "",
    )
