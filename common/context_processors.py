from django.conf import settings
from django.urls import translate_url

from common.i18n import DEFAULT_LANGUAGE, current_language

OG_LOCALES = {"en": "en_US", "uz": "uz_UZ", "ru": "ru_RU"}


def seo(request):
    """Canonical URL and hreflang alternates for the current page.

    Every page exists at /<path> (English), /uz/<path> and /ru/<path>; search
    engines need each version to point at the others."""
    lang = current_language()
    canonical = request.build_absolute_uri(request.path)
    alternates = []
    for code, _name in settings.LANGUAGES:
        alternates.append({"code": code, "url": translate_url(canonical, code)})
    x_default = translate_url(canonical, DEFAULT_LANGUAGE)
    return {
        "seo_canonical": canonical,
        "seo_alternates": alternates,
        "seo_x_default": x_default,
        "seo_og_locale": OG_LOCALES.get(lang, "en_US"),
        "seo_og_locale_alternates": [v for k, v in OG_LOCALES.items() if k != lang],
        "seo_site_root": request.build_absolute_uri("/"),
        "google_site_verification": settings.GOOGLE_SITE_VERIFICATION,
    }
