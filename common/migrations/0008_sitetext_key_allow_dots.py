"""SiteText.key was a SlugField, which rejects dots, so editing a text such as
"systems.integrated_heading" in the admin forced the key to be changed (e.g. to
"systems_integrated_heading") and the page then showed the raw key. Allow dots
and restore keys that were renamed that way."""

import django.core.validators
from django.db import migrations, models

KNOWN_KEYS = [
    "about.eyebrow",
    "about.founders_heading",
    "about.nav_title",
    "about.read_more",
    "common.learn_more",
    "contact.email_label",
    "contact.eyebrow",
    "contact.heading",
    "contact.lead",
    "contact.locations_label",
    "contact.phone_label",
    "contact.submit",
    "contact.success",
    "error404.button",
    "error404.heading",
    "error404.text",
    "footer.cta_button",
    "footer.cta_eyebrow",
    "footer.cta_heading",
    "footer.rights",
    "footer.tagline",
    "form.email",
    "form.message",
    "form.name",
    "form.phone",
    "form.too_many",
    "hero.cta_quote",
    "hero.cta_services",
    "hero.eyebrow",
    "hero.feature1",
    "hero.feature2",
    "hero.feature3",
    "hero.feature4",
    "hero.heading",
    "hero.lead",
    "howitworks.eyebrow",
    "howitworks.heading",
    "howitworks.lead",
    "howitworks.step1_desc",
    "howitworks.step1_title",
    "howitworks.step2_desc",
    "howitworks.step2_title",
    "howitworks.step3_desc",
    "howitworks.step3_title",
    "marquee.item1",
    "marquee.item2",
    "marquee.item3",
    "marquee.item4",
    "marquee.item5",
    "marquee.item6",
    "nav.about",
    "nav.contact",
    "nav.home",
    "nav.menu",
    "nav.news",
    "nav.products",
    "nav.services",
    "news.back",
    "news_page.eyebrow",
    "news_page.heading",
    "news_page.latest",
    "news_page.lead",
    "portfolio.all",
    "portfolio.heading",
    "portfolio_page.eyebrow",
    "portfolio_page.heading",
    "portfolio_page.lead",
    "pricing.heading",
    "products.back",
    "products.explore",
    "products.eyebrow",
    "products.heading",
    "products.other_heading",
    "products.request_heading",
    "products.submit",
    "products.success",
    "products_page.eyebrow",
    "products_page.heading",
    "products_page.lead",
    "seo.about_description",
    "seo.contact_description",
    "seo.default_description",
    "seo.home_title",
    "seo.news_description",
    "seo.products_description",
    "seo.services_description",
    "seo.services_title",
    "services.back",
    "services.coming_soon",
    "services.coming_soon_note",
    "services.explore",
    "services.eyebrow",
    "services.heading",
    "services.notify_me",
    "services.other_heading",
    "services_page.eyebrow",
    "services_page.heading",
    "services_page.lead",
    "systems.heading",
    "systems.integrated_heading",
    "testimonials.eyebrow",
    "whyus.eyebrow_fallback",
    "whyus.heading_fallback",
]


def restore_keys(apps, schema_editor):
    SiteText = apps.get_model("common", "SiteText")
    existing = set(SiteText.objects.values_list("key", flat=True))
    for key in KNOWN_KEYS:
        renamed = key.replace(".", "_")
        if key not in existing and renamed in existing:
            SiteText.objects.filter(key=renamed).update(key=key)


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0007_seo_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sitetext",
            name="key",
            field=models.CharField(
                help_text='e.g. "nav.home", "btn.learn_more". The site looks texts up by this exact key.',
                max_length=100,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[a-z0-9_.-]+$",
                        "Use lowercase letters, digits, dots, dashes or underscores, e.g. nav.home",
                    )
                ],
            ),
        ),
        migrations.RunPython(restore_keys, migrations.RunPython.noop),
    ]
