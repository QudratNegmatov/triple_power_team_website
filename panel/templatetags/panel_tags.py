from django import template
from django.utils.safestring import mark_safe

register = template.Library()

_PATHS = {
    "home": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/>',
    "image": '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M21 17l-5-5-9 8"/>',
    "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
    "chat": '<path d="M4 5h16v11H8l-4 4z"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5h6v2"/>',
    "tag": '<path d="M3 12V3h9l9 9-9 9z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    "box": '<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/>',
    "news": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 8h10M7 12h10M7 16h6"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
    "phone": '<path d="M5 3h4l2 5-3 2a12 12 0 006 6l2-3 5 2v4a2 2 0 01-2 2A18 18 0 013 5a2 2 0 012-2z"/>',
    "folder": '<path d="M3 6h6l2 2h10v11H3z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "inbox": '<path d="M3 13h5l1 3h6l1-3h5"/><path d="M5 5h14l2 8v6H3v-6z"/>',
    "text": '<path d="M4 6h16M4 12h10M4 18h7"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2 20c1-3.5 3.5-5 7-5s6 1.5 7 5"/><path d="M16 4a3.5 3.5 0 010 7M18 15c2 .6 3.4 2.2 4 5"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3"/>',
    "out": '<path d="M15 4h4v16h-4"/><path d="M10 8l-4 4 4 4M6 12h11"/>',
    "site": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/>',
}


@register.filter
def panel_icon(name):
    path = _PATHS.get(name, _PATHS["text"])
    return mark_safe(
        '<svg class="pi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>'
    )


@register.filter
def is_checkbox(bound_field):
    return bound_field.field.widget.input_type == "checkbox" if hasattr(bound_field.field.widget, "input_type") else False


@register.simple_tag(takes_context=True)
def page_url(context, number):
    """Current list address with another page number (keeps search and filters)."""
    params = context["request"].GET.copy()
    params["page"] = number
    return "?" + params.urlencode()
