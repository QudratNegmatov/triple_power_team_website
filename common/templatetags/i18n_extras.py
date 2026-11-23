from django import template
from django.utils.safestring import mark_safe

from common.i18n import get_site_text, get_translated

register = template.Library()


@register.simple_tag
def tr(obj, field_name):
    """Usage: {% tr service "title" %} -> service.title_<current language>"""
    return get_translated(obj, field_name)


@register.simple_tag
def tr_html(obj, field_name):
    """Same as tr, but marks the result safe for rich-text (CKEditor) fields."""
    return mark_safe(get_translated(obj, field_name))


@register.simple_tag
def st(key):
    """Usage: {% st "nav.home" %} -> the SiteText value for the current language."""
    return get_site_text(key)


@register.filter
def localize_url(url):
    """Point a site-internal link (e.g. a hero button typed as "/about/") at
    the visitor's language version ("/uz/about/"). Other links are unchanged."""
    from common.i18n import current_language

    from urllib.parse import urlsplit

    from django.conf import settings

    url = (url or "").strip()
    parts = urlsplit(url)
    if parts.netloc and parts.hostname in settings.ALLOWED_HOSTS:
        # A full link to this same site: keep only the path part.
        url = parts.path + (f"?{parts.query}" if parts.query else "") + (f"#{parts.fragment}" if parts.fragment else "")
    if not url.startswith("/") or url.startswith("//"):
        return url
    return localized_path(url, current_language())


def localized_path(url, lang):
    """"/about/" -> "/uz/about/" for lang="uz". The link may be written in any
    language's form; unknown paths are returned unchanged."""
    from urllib.parse import urlsplit, urlunsplit

    from django.conf import settings
    from django.urls import Resolver404, resolve, reverse
    from django.utils import translation

    parts = urlsplit(url)
    for code, _name in settings.LANGUAGES:
        with translation.override(code):
            try:
                match = resolve(parts.path)
            except Resolver404:
                continue
        with translation.override(lang):
            try:
                path = reverse(match.view_name, args=match.args, kwargs=match.kwargs)
            except Exception:
                return url
        return urlunsplit(("", "", path, parts.query, parts.fragment))
    return url
