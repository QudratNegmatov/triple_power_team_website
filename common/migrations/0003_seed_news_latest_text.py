from django.db import migrations

TEXTS = [
    ("news_page.latest", "News list page: badge on the featured/latest post", "Latest", "So'nggi", "Последнее"),
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
        ("common", "0002_seed_site_text"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
