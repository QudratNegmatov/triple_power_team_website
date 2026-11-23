from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from news.models import NewsPost
from products.models import Product
from services.models import Service


class I18nSitemap(Sitemap):
    """Lists every page once per language (/, /uz/, /ru/) with hreflang
    alternates, so search engines index all three language versions."""

    i18n = True
    alternates = True
    x_default = True
    protocol = "https"


class StaticPagesSitemap(I18nSitemap):
    changefreq = "weekly"

    def items(self):
        return ["home", "service_list", "product_list", "about", "news_list", "contact"]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return {"home": 1.0, "service_list": 0.9}.get(item, 0.6)


class ServiceSitemap(I18nSitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Service.objects.filter(is_active=True)

    def priority(self, obj):
        return 0.6 if obj.is_coming_soon else 0.9


class NewsSitemap(I18nSitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return NewsPost.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.published_at


class ProductSitemap(I18nSitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Product.objects.filter(is_active=True)


SITEMAPS = {
    "pages": StaticPagesSitemap,
    "services": ServiceSitemap,
    "news": NewsSitemap,
    "products": ProductSitemap,
}
