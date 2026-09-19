from django.db import migrations

SERVICES = [
    {
        "title": "Freight & Trucking",
        "slug": "freight-trucking",
        "summary": "Reliable road freight, on time, every time.",
        "description": (
            "We move your cargo by road with a modern fleet and real-time "
            "tracking, covering local and long-haul routes."
        ),
        "icon": "truck",
        "order": 1,
    },
    {
        "title": "Warehousing & Storage",
        "slug": "warehousing-storage",
        "summary": "Secure storage with flexible short and long-term space.",
        "description": (
            "Our warehouses offer secure, climate-aware storage with "
            "inventory management so your goods are always accounted for."
        ),
        "icon": "warehouse",
        "order": 2,
    },
    {
        "title": "Customs & Documentation",
        "slug": "customs-documentation",
        "summary": "Paperwork and customs clearance handled for you.",
        "description": (
            "We handle customs clearance and shipping documentation so "
            "your cargo crosses borders without delays."
        ),
        "icon": "document",
        "order": 3,
    },
]


def seed_services(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    for data in SERVICES:
        Service.objects.get_or_create(slug=data["slug"], defaults=data)


def remove_services(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    Service.objects.filter(slug__in=[d["slug"] for d in SERVICES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_services, remove_services),
    ]
