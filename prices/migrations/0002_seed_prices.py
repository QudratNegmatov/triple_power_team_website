from decimal import Decimal

from django.db import migrations

PRICES = {
    "Freight & Trucking": [
        {
            "price_type": "simple",
            "price_type_label_en": "Simple",
            "price_type_label_uz": "Oddiy",
            "price_type_label_ru": "Простой",
            "price": Decimal("0.80"),
            "period": "month",
            "features_en": "Local routes only\nStandard tracking\nEmail support",
            "features_uz": "Faqat mahalliy yo'nalishlar\nStandart kuzatuv\nEmail orqali yordam",
            "features_ru": "Только местные маршруты\nСтандартное отслеживание\nПоддержка по email",
            "order": 1,
        },
        {
            "price_type": "pro",
            "price_type_label_en": "Pro",
            "price_type_label_uz": "Pro",
            "price_type_label_ru": "Про",
            "price": Decimal("1.20"),
            "period": "month",
            "features_en": "Local and long-haul routes\nReal-time GPS tracking\nPriority phone support",
            "features_uz": "Mahalliy va uzoq masofali yo'nalishlar\nReal vaqtda GPS kuzatuvi\nUstuvor telefon orqali yordam",
            "features_ru": "Местные и дальние маршруты\nGPS-отслеживание в реальном времени\nПриоритетная поддержка по телефону",
            "order": 2,
        },
    ],
}


def seed(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    Price = apps.get_model("prices", "Price")
    for service_title, tiers in PRICES.items():
        try:
            service = Service.objects.get(title_en=service_title)
        except Service.DoesNotExist:
            continue
        for order, data in enumerate(tiers):
            Price.objects.get_or_create(
                service=service,
                price_type=data["price_type"],
                defaults={**data, "order": order},
            )


def unseed(apps, schema_editor):
    Price = apps.get_model("prices", "Price")
    Price.objects.filter(price_type__in=["simple", "pro"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("prices", "0001_initial"),
        ("services", "0002_seed_services"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
