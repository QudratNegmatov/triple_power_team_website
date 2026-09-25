from django.db import migrations

USED_SYSTEMS = {
    "Fleet Tracking": [
        {"name": "Samsara ELD", "link": "https://www.samsara.com/", "order": 1},
        {"name": "Motive", "link": "https://gomotive.com/", "order": 2},
        {"name": "Geotab", "link": "https://www.geotab.com/", "order": 3},
    ],
}

INTEGRATED_SYSTEMS = {
    "Freight & Trucking": [
        {"name": "Highway", "link": "https://www.highway.com/", "order": 1},
        {"name": "Amazon Relay", "link": "https://relay.amazon.com/", "order": 2},
    ],
}


def seed(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    UsedSystem = apps.get_model("services", "UsedSystem")
    IntegratedSystem = apps.get_model("services", "IntegratedSystem")

    for service_title, systems in USED_SYSTEMS.items():
        try:
            service = Service.objects.get(title_en=service_title)
        except Service.DoesNotExist:
            continue
        for data in systems:
            UsedSystem.objects.get_or_create(service=service, name=data["name"], defaults=data)

    for service_title, systems in INTEGRATED_SYSTEMS.items():
        try:
            service = Service.objects.get(title_en=service_title)
        except Service.DoesNotExist:
            continue
        for data in systems:
            IntegratedSystem.objects.get_or_create(service=service, name=data["name"], defaults=data)


def unseed(apps, schema_editor):
    UsedSystem = apps.get_model("services", "UsedSystem")
    IntegratedSystem = apps.get_model("services", "IntegratedSystem")
    names = [s["name"] for systems in USED_SYSTEMS.values() for s in systems]
    UsedSystem.objects.filter(name__in=names).delete()
    names = [s["name"] for systems in INTEGRATED_SYSTEMS.values() for s in systems]
    IntegratedSystem.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0003_integratedsystem_usedsystem"),
        ("services", "0002_seed_services"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
