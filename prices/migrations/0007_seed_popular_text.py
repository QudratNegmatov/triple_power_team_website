from django.db import migrations


def seed(apps, schema_editor):
    SiteText = apps.get_model("common", "SiteText")
    SiteText.objects.get_or_create(
        key="pricing.popular",
        defaults={
            "description": 'Badge on the plan marked "Most popular"',
            "value_en": "Most popular",
            "value_uz": "Eng ko'p tanlanadi",
            "value_ru": "Самый популярный",
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ("prices", "0006_price_is_featured"),
        ("common", "0008_sitetext_key_allow_dots"),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
