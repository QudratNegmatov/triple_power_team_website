import io

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from common.models import SiteText
from core.models import ContactMessage, HeroSlide
from panel.registry import resources
from prices.models import Price
from services.models import Service, UsedSystem


def tiny_png():
    from PIL import Image

    buf = io.BytesIO()
    Image.new("RGB", (4, 4), (34, 197, 94)).save(buf, "PNG")
    return SimpleUploadedFile("pic.png", buf.getvalue(), content_type="image/png")


@override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.InMemoryStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class PanelTests(TestCase):
    def setUp(self):
        cache.clear()
        User = get_user_model()
        self.owner = User.objects.create_user("owner", password="pass-12345", is_staff=True, is_superuser=True)
        self.client.login(username="owner", password="pass-12345")

    def test_requires_staff_login(self):
        self.client.logout()
        response = self.client.get("/admin/services/")
        self.assertRedirects(response, "/admin/login/?next=/admin/services/")
        get_user_model().objects.create_user("visitor", password="pass-12345")
        self.client.login(username="visitor", password="pass-12345")
        self.assertEqual(self.client.get("/admin/").status_code, 302)

    def test_login_page_and_wrong_password(self):
        self.client.logout()
        response = self.client.post("/admin/login/", {"username": "owner", "password": "nope"})
        self.assertContains(response, "Login yoki parol noto")
        response = self.client.post("/admin/login/", {"username": "owner", "password": "pass-12345"})
        self.assertRedirects(response, "/admin/")

    def test_every_page_opens(self):
        for url in ["/admin/", "/admin/password/", "/admin/users/", "/admin/users/add/"]:
            self.assertEqual(self.client.get(url).status_code, 200, url)
        for slug, resource in resources().items():
            self.assertEqual(self.client.get(f"/admin/{slug}/").status_code, 200, slug)
            self.assertEqual(self.client.get(f"/admin/{slug}/?q=a&active=1").status_code, 200, slug)
            obj = resource.model.objects.first()
            if obj:
                self.assertEqual(self.client.get(f"/admin/{slug}/{obj.pk}/").status_code, 200, slug)
            if resource.can_add and not resource.readonly:
                self.assertEqual(self.client.get(f"/admin/{slug}/add/").status_code, 200, slug)
        self.assertEqual(self.client.get("/admin/services/not-a-uuid/").status_code, 404)

    def test_create_hero_slide_with_image(self):
        data = {
            "title_en": "Hello", "title_uz": "Salom", "title_ru": "Привет",
            "description_en": "d", "description_uz": "d", "description_ru": "d",
            "button_name_en": "", "button_name_uz": "", "button_name_ru": "", "button_url": "",
            "order": "5", "is_active": "on", "image": tiny_png(),
        }
        response = self.client.post("/admin/hero/add/", data)
        self.assertRedirects(response, "/admin/hero/")
        slide = HeroSlide.objects.get(title_en="Hello")
        self.assertEqual(slide.title_uz, "Salom")
        self.assertEqual(slide.created_by, self.owner)
        self.assertTrue(slide.image)

    def test_missing_translation_shows_error(self):
        response = self.client.post("/admin/hero/add/", {"title_en": "Only English", "order": "0"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Saqlanmadi")
        self.assertFalse(HeroSlide.objects.filter(title_en="Only English").exists())

    def _service_post(self, service, **extra):
        data = {}
        form_names = resources()["services"].form_fields()
        for name in form_names:
            value = getattr(service, name)
            if isinstance(value, bool):
                if value:
                    data[name] = "on"
            else:
                data[name] = "" if value is None else str(value)
        for inline in resources()["services"].inlines:
            items = list(getattr(service, inline.name).all())
            data[f"{inline.name}-TOTAL_FORMS"] = str(len(items))
            data[f"{inline.name}-INITIAL_FORMS"] = str(len(items))
            for i, item in enumerate(items):
                data[f"{inline.name}-{i}-id"] = str(item.pk)
                data[f"{inline.name}-{i}-service"] = str(service.pk)
                for name in ("name", "link", "order"):
                    if hasattr(item, name):
                        data[f"{inline.name}-{i}-{name}"] = str(getattr(item, name))
                if item.is_active:
                    data[f"{inline.name}-{i}-is_active"] = "on"
        data.update(extra)
        return data

    def test_edit_service_and_add_inline_system(self):
        service = Service.objects.get(slug="eld-service")
        used = service.used_systems.count()
        n = used
        data = self._service_post(
            service,
            title_uz="ELD xizmati (yangi)",
            full_info_en="<p><b>Bold</b> text</p>",
            **{
                "used_systems-TOTAL_FORMS": str(used + 1),
                f"used_systems-{n}-name": "NewELD",
                f"used_systems-{n}-order": "9",
                f"used_systems-{n}-is_active": "on",
                f"used_systems-{n}-link": "",
            },
        )
        response = self.client.post(f"/admin/services/{service.pk}/", data)
        self.assertRedirects(response, "/admin/services/")
        service.refresh_from_db()
        self.assertEqual(service.title_uz, "ELD xizmati (yangi)")
        self.assertEqual(service.full_info_en, "<p><b>Bold</b> text</p>")
        self.assertTrue(UsedSystem.objects.filter(service=service, name="NewELD", created_by=self.owner).exists())

    def test_delete_inline_item(self):
        service = Service.objects.get(slug="eld-service")
        first = service.used_systems.first()
        data = self._service_post(service, **{"used_systems-0-DELETE": "on"})
        self.client.post(f"/admin/services/{service.pk}/", data)
        self.assertFalse(UsedSystem.objects.filter(pk=first.pk).exists())

    def test_toggle_and_delete(self):
        price = Price.objects.first()
        self.client.post(f"/admin/prices/{price.pk}/toggle/", {"next": "/admin/prices/"})
        price.refresh_from_db()
        self.assertFalse(price.is_active)
        self.client.post(f"/admin/prices/{price.pk}/delete/")
        self.assertFalse(Price.objects.filter(pk=price.pk).exists())

    def test_toggle_rejects_outside_redirect(self):
        price = Price.objects.first()
        response = self.client.post(f"/admin/prices/{price.pk}/toggle/", {"next": "https://evil.example/"})
        self.assertRedirects(response, "/admin/prices/", fetch_redirect_response=False)

    def test_messages_are_read_only(self):
        msg = ContactMessage.objects.create(name="Ali", email="ali@example.com", message="Salom")
        response = self.client.get(f"/admin/messages/{msg.pk}/")
        self.assertContains(response, "ali@example.com")
        self.assertNotContains(response, "<form method=\"post\" enctype")
        self.assertEqual(self.client.get("/admin/messages/add/").status_code, 404)

    def test_site_text_key_cannot_change(self):
        text = SiteText.objects.get(key="nav.home")
        response = self.client.post(f"/admin/site-texts/{text.pk}/", {
            "key": "hacked", "value_en": "Home!", "value_uz": "Bosh", "value_ru": "Главная"})
        self.assertRedirects(response, "/admin/site-texts/")
        text.refresh_from_db()
        self.assertEqual((text.key, text.value_en), ("nav.home", "Home!"))

    def test_users_and_password(self):
        response = self.client.post("/admin/users/add/", {
            "username": "editor", "email": "e@example.com",
            "password1": "Very-strong-pass-91", "password2": "Very-strong-pass-91"})
        self.assertRedirects(response, "/admin/users/")
        editor = get_user_model().objects.get(username="editor")
        self.assertTrue(editor.is_staff)
        self.assertFalse(editor.is_superuser)
        # An editor cannot manage administrators.
        self.client.logout()
        self.client.login(username="editor", password="Very-strong-pass-91")
        self.assertEqual(self.client.get("/admin/users/").status_code, 403)
        self.assertEqual(self.client.get("/admin/services/").status_code, 200)

    def test_csp_header_on_panel(self):
        response = self.client.get("/admin/")
        self.assertIn("script-src 'self'", response["Content-Security-Policy"])
