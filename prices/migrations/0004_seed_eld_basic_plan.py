"""ELD Basic plan ($79.99 per truck per month) and the texts of the pricing
section. Nothing is overwritten if the admin already changed it."""

from decimal import Decimal

from django.db import migrations

TEXTS = [
    ("pricing.subheading", "Pricing section: line under the heading",
     "You can even use our demo version to check the whole system.",
     "Butun tizimni sinab ko'rish uchun demo versiyadan ham foydalanishingiz mumkin.",
     "Вы можете проверить всю систему в нашей демо-версии."),
    ("pricing.cta", "Pricing card button",
     "Get started", "Boshlash", "Начать"),
    ("pricing.period_month", "Pricing card: shown under the price when the plan has no own note",
     "Per month", "Oyiga", "В месяц"),
    ("pricing.period_year", "Pricing card: yearly plans",
     "Per year", "Yiliga", "В год"),
    ("pricing.period_one_time", "Pricing card: one-time price",
     "One-time payment", "Bir martalik to'lov", "Разовый платёж"),
    ("pricing.plan_interest", "Pre-filled contact message when a plan's button is clicked",
     "I'm interested in the plan:", "Meni qiziqtirgan tarif:", "Меня интересует тариф:"),
]

BASIC_PLAN = {
    "price_type": "basic",
    "price_type_label_en": "Basic Plan",
    "price_type_label_uz": "Asosiy tarif",
    "price_type_label_ru": "Базовый тариф",
    "price": Decimal("79.99"),
    "period": "month",
    "note_en": "Per month for a truck",
    "note_uz": "Bir truck uchun oyiga",
    "note_ru": "В месяц за один трак",
    "features_en": "Electronic Logbook\nElectronic DVIR\nFleet Manager Portal\nGPS Fleet Tracking\nIFTA Reporting\nLogbook Monitoring\n24/7 support",
    "features_uz": "Elektron logbook\nElektron DVIR\nFleet menejer portali\nGPS orqali avtopark kuzatuvi\nIFTA hisobotlari\nLogbook monitoringi\n24/7 yordam",
    "features_ru": "Электронный логбук\nЭлектронный DVIR\nПортал менеджера автопарка\nGPS-отслеживание автопарка\nОтчёты IFTA\nМониторинг логбука\nПоддержка 24/7",
    "order": 0,
}


def seed(apps, schema_editor):
    SiteText = apps.get_model("common", "SiteText")
    for key, description, en, uz, ru in TEXTS:
        SiteText.objects.get_or_create(
            key=key, defaults={"description": description, "value_en": en, "value_uz": uz, "value_ru": ru}
        )
    # "Pricing" -> "Pricing Plans", unless the admin already changed it.
    SiteText.objects.filter(key="pricing.heading", value_en="Pricing").update(
        value_en="Pricing Plans", value_uz="Tariflar", value_ru="Тарифы"
    )

    Service = apps.get_model("services", "Service")
    Price = apps.get_model("prices", "Price")
    eld = Service.objects.filter(title_en="ELD Service").first()
    if eld and not Price.objects.filter(service=eld).exists():
        Price.objects.create(service=eld, **BASIC_PLAN)


class Migration(migrations.Migration):

    dependencies = [
        ("prices", "0003_price_note"),
        ("common", "0008_sitetext_key_allow_dots"),
        ("services", "0007_service_slug"),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
