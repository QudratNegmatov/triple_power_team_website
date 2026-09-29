from django.db import migrations

TEXTS = [
    ("products.eyebrow", "Homepage products section eyebrow", "Shop", "Do'kon", "Магазин"),
    ("products.heading", "Homepage products section heading", "Equipment & Products", "Uskunalar va mahsulotlar", "Оборудование и товары"),
    ("products.explore", "Button: Explore all products", "Explore all products", "Barcha mahsulotlarni ko'rish", "Смотреть все товары"),
]


def seed(apps, schema_editor):
    SiteText = apps.get_model("common", "SiteText")
    for key, description, value_en, value_uz, value_ru in TEXTS:
        SiteText.objects.get_or_create(
            key=key,
            defaults={
                "description": description,
                "value_en": value_en,
                "value_uz": value_uz,
                "value_ru": value_ru,
            },
        )


def unseed(apps, schema_editor):
    SiteText = apps.get_model("common", "SiteText")
    SiteText.objects.filter(key__in=[key for key, *_ in TEXTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0003_seed_news_latest_text"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
