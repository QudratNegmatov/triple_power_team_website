from django import template
from django.utils.safestring import mark_safe

register = template.Library()

_STROKE = 'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'

ICONS = {
    "truck": f'''<svg viewBox="0 0 24 24" {_STROKE}>
        <path d="M1 4h13v11H1z"/><path d="M14 8h4l4 4v3h-8z"/>
        <circle cx="5.5" cy="17.5" r="1.8"/><circle cx="17.5" cy="17.5" r="1.8"/>
    </svg>''',
    "warehouse": f'''<svg viewBox="0 0 24 24" {_STROKE}>
        <path d="M2 10 12 3l10 7"/><path d="M4 9v11h16V9"/>
        <path d="M9 20v-6h6v6"/>
    </svg>''',
    "document": f'''<svg viewBox="0 0 24 24" {_STROKE}>
        <path d="M6 2h9l4 4v16H6z"/><path d="M15 2v4h4"/>
        <path d="M9 12h6M9 16h6M9 8h3"/>
    </svg>''',
    "globe": f'''<svg viewBox="0 0 24 24" {_STROKE}>
        <circle cx="12" cy="12" r="9"/><path d="M3 12h18"/>
        <path d="M12 3c2.7 2.6 4 5.7 4 9s-1.3 6.4-4 9c-2.7-2.6-4-5.7-4-9s1.3-6.4 4-9z"/>
    </svg>''',
    "package": f'''<svg viewBox="0 0 24 24" {_STROKE}>
        <path d="M3 7.5 12 3l9 4.5-9 4.5-9-4.5z"/>
        <path d="M3 7.5V17l9 4.5 9-4.5V7.5"/><path d="M12 12v9.5"/>
    </svg>''',
}


@register.filter
def svg_icon(name):
    return mark_safe(ICONS.get(name, ICONS["package"]))
