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
