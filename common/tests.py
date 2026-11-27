import time

from django.core import signing
from django.core.cache import cache
from django.test import TestCase, override_settings

from core.models import ContactMessage, HeroSlide
from news.models import NewsPost
from services.models import Service


@override_settings(ALLOWED_HOSTS=["testserver", "example.com"])
class SeoTests(TestCase):
    def setUp(self):
        cache.clear()
        self.service = Service.objects.filter(is_active=True).first()

    def test_language_urls(self):
        for url in ["/", "/uz/", "/ru/", "/services/", "/uz/about/", "/ru/contact/"]:
            self.assertEqual(self.client.get(url).status_code, 200, url)
        self.assertContains(self.client.get("/uz/"), '<html lang="uz">')
        self.assertContains(self.client.get("/ru/"), '<html lang="ru">')

    def test_hreflang_and_canonical(self):
        page = self.client.get("/uz/services/").content.decode()
        self.assertIn('<link rel="canonical" href="http://testserver/uz/services/">', page)
        self.assertIn('hreflang="en" href="http://testserver/services/"', page)
        self.assertIn('hreflang="ru" href="http://testserver/ru/services/"', page)
        self.assertIn('hreflang="x-default" href="http://testserver/services/"', page)
        self.assertIn('application/ld+json', page)

    def test_slug_url_and_uuid_redirect(self):
        self.assertTrue(self.service.slug)
        self.assertEqual(self.client.get(f"/ru/services/{self.service.slug}/").status_code, 200)
        response = self.client.get(f"/ru/services/{self.service.pk}/")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], f"/ru/services/{self.service.slug}/")

    def test_every_detail_page_renders(self):
        from django.utils import translation

        from products.models import Product

        for obj in [*Service.objects.all(), *NewsPost.objects.all(), *Product.objects.all()]:
            for lang in ("en", "uz", "ru"):
                with translation.override(lang):
                    url = obj.get_absolute_url()
                self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_news_slug(self):
        post = NewsPost.objects.filter(is_active=True).first()
        self.assertEqual(self.client.get(post.get_absolute_url()).status_code, 200)

    def test_sitemap_and_robots(self):
        sitemap = self.client.get("/sitemap.xml").content.decode()
        self.assertIn(f"/uz/services/{self.service.slug}/", sitemap)
        self.assertIn('hreflang="x-default"', sitemap)
        robots = self.client.get("/robots.txt").content.decode()
        self.assertIn("Sitemap: http://testserver/sitemap.xml", robots)
        self.assertIn("Disallow: /admin/", robots)

    def test_404_page_is_noindex(self):
        response = self.client.get("/uz/no-such-page/")
        self.assertEqual(response.status_code, 404)

    def test_hero_button_link_follows_language(self):
        HeroSlide.objects.create(
            title_en="T", title_uz="T", title_ru="T",
            description_en="D", description_uz="D", description_ru="D",
            button_name_en="More", button_name_uz="Batafsil", button_name_ru="Ещё",
            button_url="http://example.com/about/",
        )
        self.assertContains(self.client.get("/uz/"), 'href="/uz/about/" class="btn btn-ghost"')

    def test_security_headers(self):
        response = self.client.get("/")
        self.assertIn("default-src 'self'", response["Content-Security-Policy"])
        self.assertIn("camera=()", response["Permissions-Policy"])


class ContactFormTests(TestCase):
    def setUp(self):
        cache.clear()

    def _data(self, age=10, **extra):
        data = {
            "name": "Ali",
            "email": "ali@example.com",
            "message": "Hello",
            "website": "",
            "ts": signing.dumps(int(time.time()) - age, salt="form-ts"),
        }
        data.update(extra)
        return data

    def test_labels_are_translated(self):
        self.assertContains(self.client.get("/uz/contact/"), "Ismingiz")
        self.assertContains(self.client.get("/ru/contact/"), "Сообщение")

    def test_real_message_is_saved(self):
        self.client.post("/contact/", self._data())
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_honeypot_and_fast_bots_are_dropped(self):
        self.client.post("/contact/", self._data(website="http://spam.example"))
        self.client.post("/contact/", self._data(age=0))
        self.client.post("/contact/", self._data(ts="forged"))
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_rate_limit(self):
        for _ in range(8):
            self.client.post("/contact/", self._data())
        self.assertEqual(ContactMessage.objects.count(), 5)


class AdminLoginThrottleTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_blocks_after_repeated_failures(self):
        codes = [
            self.client.post("/admin/login/", {"username": "x", "password": "y"}).status_code
            for _ in range(9)
        ]
        self.assertEqual(codes[-1], 429)


class PricingAndSiteTextTests(TestCase):
    def test_pricing_cards_on_home_and_service_page(self):
        from prices.models import Price

        plan = Price.objects.get(price_type="basic")
        for url in ("/", plan.service.get_absolute_url(), "/uz/", "/ru/"):
            page = self.client.get(url).content.decode()
            self.assertIn('class="pricing-card', page, url)
        page = self.client.get("/").content.decode()
        self.assertIn("$79<sup>.99</sup>", page)
        self.assertIn("Per month for a truck", page)
        self.assertIn("Electronic DVIR", page)
        self.assertIn("Elektron DVIR", self.client.get("/uz/").content.decode())

    def test_plan_button_prefills_contact_message(self):
        from prices.models import Price

        plan = Price.objects.get(price_type="basic")
        self.assertContains(self.client.get(f"/contact/?plan={plan.pk}"), "Basic Plan — ELD Service")
        self.assertEqual(self.client.get("/contact/?plan=not-a-uuid").status_code, 200)

    def test_every_text_key_in_templates_exists(self):
        import re
        from pathlib import Path

        from django.conf import settings

        from common.models import SiteText

        keys = set()
        for path in Path(settings.BASE_DIR).glob("**/templates/**/*.html"):
            keys |= set(re.findall(r'\{% st "([^"]+)"', path.read_text()))
        missing = keys - set(SiteText.objects.values_list("key", flat=True))
        self.assertEqual(missing, set())

    def test_underscore_key_still_found(self):
        from common.i18n import get_site_text
        from common.models import SiteText

        text = SiteText.objects.get(key="systems.integrated_heading")
        text.key = "systems_integrated_heading"
        text.save()
        from django.utils import translation

        with translation.override("en"):
            self.assertEqual(get_site_text("systems.integrated_heading"), text.value_en)

    def test_admin_cannot_rename_key(self):
        from django.contrib.admin.sites import site

        from common.models import SiteText

        admin = site._registry[SiteText]
        self.assertIn("key", admin.get_readonly_fields(None, SiteText.objects.first()))
