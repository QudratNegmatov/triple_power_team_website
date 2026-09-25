from django.db import migrations

PROJECTS = [
    {
        "title_en": "Nationwide Retail Distribution",
        "title_uz": "Butun mamlakat bo'ylab chakana savdo distributsiyasi",
        "title_ru": "Общенациональная розничная дистрибуция",
        "summary_en": "Multi-region distribution network for a retail chain.",
        "summary_uz": "Chakana savdo tarmog'i uchun ko'p mintaqali distributsiya tarmog'i.",
        "summary_ru": "Многорегиональная сеть дистрибуции для розничной сети.",
        "description_en": "Set up a distribution network across multiple regions, cutting average delivery time significantly.",
        "description_uz": "Bir nechta mintaqalarda distributsiya tarmog'ini yo'lga qo'ydik, o'rtacha yetkazib berish vaqtini sezilarli qisqartirdik.",
        "description_ru": "Создали сеть дистрибуции в нескольких регионах, значительно сократив среднее время доставки.",
        "client": "Retail Client",
        "order": 1,
    },
    {
        "title_en": "Cold Chain Expansion",
        "title_uz": "Sovuq zanjirni kengaytirish",
        "title_ru": "Расширение холодовой цепи",
        "summary_en": "Temperature-controlled storage and transport rollout.",
        "summary_uz": "Harorat nazorati ostidagi saqlash va tashish tizimini joriy qilish.",
        "summary_ru": "Внедрение хранения и перевозки с контролем температуры.",
        "description_en": "Expanded cold storage and refrigerated transport capacity for a food distributor.",
        "description_uz": "Oziq-ovqat distributor kompaniyasi uchun sovutgichli saqlash va tashish quvvatini kengaytirdik.",
        "description_ru": "Расширили мощности холодного хранения и перевозки для дистрибьютора продуктов питания.",
        "client": "Food Distributor",
        "order": 2,
    },
    {
        "title_en": "Port-to-Door Import Program",
        "title_uz": "Portdan eshikkacha import dasturi",
        "title_ru": "Программа импорта «от порта до двери»",
        "summary_en": "End-to-end import handling from port to final delivery.",
        "summary_uz": "Portdan yakuniy yetkazib berishgacha to'liq import xizmati.",
        "summary_ru": "Полное сопровождение импорта от порта до конечной доставки.",
        "description_en": "Managed customs clearance, warehousing, and last-mile delivery for an importer.",
        "description_uz": "Importyor uchun bojxona rasmiylashtiruvi, omborxona va oxirgi bosqich yetkazib berishni boshqardik.",
        "description_ru": "Организовали таможенную очистку, складирование и доставку последней мили для импортёра.",
        "client": "Import Business",
        "order": 3,
    },
]


def seed(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    for data in PROJECTS:
        Project.objects.create(**data)


def unseed(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    Project.objects.filter(title_en__in=[p["title_en"] for p in PROJECTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
