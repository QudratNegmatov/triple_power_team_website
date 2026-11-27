import json

from django import template
from django.templatetags.static import static
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.text import Truncator

from common.i18n import get_translated

register = template.Library()


@register.filter
def meta_text(value, length=160):
    """Plain text for <meta name="description">: no HTML, no line breaks, max ~160 chars."""
    text = " ".join(strip_tags(str(value or "")).split())
    return Truncator(text).chars(int(length))


def _json_script(data):
    # Escape "<" so text from the admin can never close the <script> tag early.
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    return mark_safe(f'<script type="application/ld+json">{payload}</script>')


def _abs(request, url):
    return url if url.startswith("http") else request.build_absolute_uri(url)


def _organization(request, contact):
    org = {
        "@type": "ProfessionalService",
        "@id": request.build_absolute_uri("/#organization"),
        "name": "Triple Power Team",
        "url": request.build_absolute_uri("/"),
        "logo": request.build_absolute_uri(static("img/logo-512.png")),
        "image": request.build_absolute_uri(static("img/og-image.png")),
        "description": "ELD service, HOS compliance, DOT audit support and truck dispatch for US trucking companies and owner-operators.",
        "areaServed": {"@type": "Country", "name": "United States"},
        "availableLanguage": ["English", "Uzbek", "Russian"],
        "openingHours": "Mo-Su 00:00-23:59",
        "knowsAbout": ["ELD", "Hours of Service", "DOT audit", "IFTA", "Truck dispatch"],
    }
    if contact:
        if contact.email:
            org["email"] = contact.email
        if contact.phone:
            org["telephone"] = contact.phone
        location = contact.locations.first()
        if location:
            org["address"] = location.address_en
    return org


@register.simple_tag(takes_context=True)
def jsonld_site(context):
    """Organization + WebSite structured data, shown on every page."""
    request = context["request"]
    graph = [
        _organization(request, context.get("site_contact_info")),
        {
            "@type": "WebSite",
            "@id": request.build_absolute_uri("/#website"),
            "url": request.build_absolute_uri("/"),
            "name": "Triple Power Team",
            "inLanguage": ["en", "uz", "ru"],
            "publisher": {"@id": request.build_absolute_uri("/#organization")},
        },
    ]
    return _json_script({"@context": "https://schema.org", "@graph": graph})


@register.simple_tag(takes_context=True)
def jsonld_service(context, service):
    request = context["request"]
    data = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": get_translated(service, "title"),
        "description": meta_text(get_translated(service, "short_name"), 300),
        "serviceType": service.title_en,
        "url": request.build_absolute_uri(request.path),
        "provider": {"@id": request.build_absolute_uri("/#organization")},
        "areaServed": {"@type": "Country", "name": "United States"},
    }
    offers = [
        {
            "@type": "Offer",
            "name": get_translated(price, "price_type_label"),
            "price": f"{price.price:.2f}",
            "priceCurrency": "USD",
            "url": request.build_absolute_uri(request.path),
        }
        for price in context.get("prices") or []
    ]
    if offers:
        data["offers"] = offers
    return _json_script(data)


@register.simple_tag(takes_context=True)
def jsonld_article(context, post, image_url=""):
    request = context["request"]
    data = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": get_translated(post, "title")[:110],
        "description": meta_text(get_translated(post, "excerpt"), 300),
        "datePublished": post.published_at.isoformat(),
        "dateModified": post.published_at.isoformat(),
        "mainEntityOfPage": request.build_absolute_uri(request.path),
        "author": {"@id": request.build_absolute_uri("/#organization")},
        "publisher": {"@id": request.build_absolute_uri("/#organization")},
        "image": [_abs(request, image_url or static("img/og-image.png"))],
    }
    return _json_script(data)


@register.simple_tag(takes_context=True)
def jsonld_product(context, product, image_url=""):
    request = context["request"]
    price = product.discount_price or product.price
    data = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": get_translated(product, "title"),
        "description": meta_text(get_translated(product, "description"), 300),
        "image": [_abs(request, image_url or static("img/og-image.png"))],
        "brand": {"@type": "Brand", "name": "Triple Power Team"},
        "offers": {
            "@type": "Offer",
            "price": f"{price:.2f}",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "url": request.build_absolute_uri(request.path),
        },
    }
    return _json_script(data)


@register.simple_tag(takes_context=True)
def jsonld_breadcrumbs(context, *pairs):
    """{% jsonld_breadcrumbs "Services" services_url service_title "" %} - label/url pairs;
    an empty url means the current page."""
    request = context["request"]
    items = []
    for i in range(0, len(pairs) - 1, 2):
        label, url = pairs[i], pairs[i + 1]
        items.append(
            {
                "@type": "ListItem",
                "position": len(items) + 1,
                "name": str(label),
                "item": _abs(request, url) if url else request.build_absolute_uri(request.path),
            }
        )
    return _json_script({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})
