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
    "map-pin": f'''<svg viewBox="0 0 24 24" {_STROKE}>
        <path d="M12 21s7-6.5 7-12a7 7 0 1 0-14 0c0 5.5 7 12 7 12z"/>
        <circle cx="12" cy="9" r="2.5"/>
    </svg>''',
    "shield": f'''<svg viewBox="0 0 24 24" {_STROKE}>
        <path d="M12 2 4 5v6c0 5 3.5 8.5 8 11 4.5-2.5 8-6 8-11V5z"/>
        <path d="M9 12l2 2 4-4"/>
    </svg>''',
    "dashboard": f'''<svg viewBox="0 0 24 24" {_STROKE}>
        <rect x="3" y="4" width="18" height="12" rx="2"/>
        <path d="M8 20h8M12 16v4"/><path d="M7 12l3-3 3 2 4-4"/>
    </svg>''',
    "check": f'''<svg viewBox="0 0 24 24" {_STROKE}>
        <circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.5 2.5L16 9.5"/>
    </svg>''',
    "clock": f'''<svg viewBox="0 0 24 24" {_STROKE}>
        <circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>
    </svg>''',
    "users": f'''<svg viewBox="0 0 24 24" {_STROKE}>
        <circle cx="9" cy="8" r="3"/><path d="M2.5 20c0-3.5 3-6 6.5-6s6.5 2.5 6.5 6"/>
        <circle cx="17.5" cy="9" r="2.3"/><path d="M15.5 14.3c2.6.4 4.5 2.4 4.5 5.7"/>
    </svg>''',
    "star": f'''<svg viewBox="0 0 24 24" {_STROKE}>
        <path d="M12 3l2.6 5.6 6.1.6-4.6 4.1 1.3 6-5.4-3.1-5.4 3.1 1.3-6-4.6-4.1 6.1-.6z"/>
    </svg>''',
    "arrow-right": f'''<svg viewBox="0 0 24 24" {_STROKE}>
        <path d="M4 12h15M13 6l6 6-6 6"/>
    </svg>''',
}


@register.filter
def svg_icon(name):
    return mark_safe(ICONS.get(name, ICONS["package"]))
