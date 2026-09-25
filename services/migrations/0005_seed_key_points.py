from django.db import migrations

KEY_POINTS = {
    "freight-trucking": [
        "Local and long-haul routes",
        "Real-time GPS tracking on every load",
        "Modern, well-maintained fleet",
    ],
    "warehousing-storage": [
        "Secure, monitored facilities",
        "Short-term and long-term storage options",
        "Live inventory management",
    ],
    "customs-documentation": [
        "Full import/export documentation handled",
        "Experienced customs clearance team",
        "Fewer delays at the border",
    ],
    "fleet-tracking": [
        "Live GPS location for every vehicle",
        "Accurate ETAs shared with your customers",
        "Delivery history and reporting",
    ],
}


def seed_key_points(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    for slug, points in KEY_POINTS.items():
        Service.objects.filter(slug=slug).update(key_points="\n".join(points))


def unseed_key_points(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    Service.objects.filter(slug__in=KEY_POINTS.keys()).update(key_points="")


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0004_service_image_service_key_points"),
    ]

    operations = [
        migrations.RunPython(seed_key_points, unseed_key_points),
    ]
