from decimal import Decimal

from django.db import migrations

PRODUCTS = [
    {
        "title_en": "ELD Device — Standard",
        "title_uz": "ELD qurilma — Standart",
        "title_ru": "ELD-устройство — Стандарт",
        "description_en": "FMCSA-compliant electronic logging device for single vehicles. Plug-and-play installation with automatic hours-of-service tracking.",
        "description_uz": "Bitta transport vositasi uchun FMCSA talablariga javob beradigan elektron jurnal qurilmasi. O'rnatish oson, ish soatlari avtomatik kuzatiladi.",
        "description_ru": "Электронное устройство регистрации, соответствующее требованиям FMCSA, для одного автомобиля. Простая установка и автоматический учёт часов работы.",
        "price": Decimal("149.00"),
        "discount_price": None,
        "order": 1,
    },
    {
        "title_en": "ELD Device — Pro Fleet",
        "title_uz": "ELD qurilma — Pro avtopark",
        "title_ru": "ELD-устройство — Pro для автопарка",
        "description_en": "Our advanced ELD unit built for fleet operators: live GPS tracking, driver behavior reports, and fleet dashboard access included.",
        "description_uz": "Avtopark operatorlari uchun ilg'or ELD qurilmasi: jonli GPS kuzatuvi, haydovchi xatti-harakati hisobotlari va boshqaruv paneli kiritilgan.",
        "description_ru": "Продвинутое ELD-устройство для автопарков: GPS-отслеживание в реальном времени, отчёты о поведении водителя и доступ к панели управления.",
        "price": Decimal("219.00"),
        "discount_price": Decimal("179.00"),
        "order": 2,
    },
    {
        "title_en": "GPS Fleet Tracker",
        "title_uz": "GPS avtopark kuzatuvchisi",
        "title_ru": "GPS-трекер для автопарка",
        "description_en": "Standalone GPS tracking unit for trailers and equipment. Real-time location updates and geofencing alerts.",
        "description_uz": "Tirkamalar va uskunalar uchun mustaqil GPS kuzatuv qurilmasi. Real vaqtda joylashuv va geofencing ogohlantirishlari.",
        "description_ru": "Автономный GPS-трекер для прицепов и оборудования. Обновления местоположения в реальном времени и геозоны.",
        "price": Decimal("89.00"),
        "discount_price": None,
        "order": 3,
    },
]


def seed(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    for data in PRODUCTS:
        Product.objects.create(**data)


def unseed(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    Product.objects.filter(title_en__in=[p["title_en"] for p in PRODUCTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
