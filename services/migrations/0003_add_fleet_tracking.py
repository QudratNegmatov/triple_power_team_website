from django.db import migrations

SERVICE = {
    "title": "Fleet Tracking",
    "slug": "fleet-tracking",
    "summary": "Live GPS tracking and ETAs for every shipment.",
    "description": (
        "Track every vehicle in real time and share accurate ETAs with "
        "your customers from pickup to final delivery."
    ),
    "icon": "map-pin",
    "order": 4,
}


def seed_service(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    Service.objects.get_or_create(slug=SERVICE["slug"], defaults=SERVICE)


def remove_service(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    Service.objects.filter(slug=SERVICE["slug"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0002_seed_services"),
    ]

    operations = [
        migrations.RunPython(seed_service, remove_service),
    ]
