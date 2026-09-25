from django import template
from django.utils.safestring import mark_safe

from common.i18n import get_translated

register = template.Library()


@register.simple_tag
def tr(obj, field_name):
    """Usage: {% tr service "title" %} -> service.title_<current language>"""
    return get_translated(obj, field_name)


@register.simple_tag
def tr_html(obj, field_name):
    """Same as tr, but marks the result safe for rich-text (CKEditor) fields."""
    return mark_safe(get_translated(obj, field_name))
