from django.utils import translation

SUPPORTED_LANGUAGES = ("en", "uz", "ru")
DEFAULT_LANGUAGE = "en"


def current_language():
    lang = (translation.get_language() or DEFAULT_LANGUAGE).split("-")[0]
    return lang if lang in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE


def get_translated(obj, base_name):
    """Return obj.<base_name>_<current lang>, falling back to the English field."""
    lang = current_language()
    value = getattr(obj, f"{base_name}_{lang}", None)
    if value:
        return value
    return getattr(obj, f"{base_name}_{DEFAULT_LANGUAGE}", "")


def get_site_text(key):
    """Look up a SiteText value by key for the current language.

    Caches every SiteText row for 5 minutes (the model clears this cache on
    save/delete, so admin edits still show up immediately).
    """
    from django.core.cache import cache

    from common.models import SiteText

    texts = cache.get("site_text_all")
    if texts is None:
        texts = {t.key: t for t in SiteText.objects.all()}
        cache.set("site_text_all", texts, 300)
    obj = texts.get(key)
    if obj is None:
        return key
    return get_translated(obj, "value")
