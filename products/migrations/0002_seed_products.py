from decimal import Decimal

from django.db import migrations

PRODUCTS = [
    {
        "title": "ELD Device — Standard",
        "slug": "eld-device-standard",
        "description": (
            "FMCSA-compliant electronic logging device for single vehicles. "
            "Plug-and-play installation with automatic hours-of-service "
            "tracking."
        ),
        "price": Decimal("149.00"),
        "discount_price": None,
        "order": 1,
    },
    {
        "title": "ELD Device — Pro Fleet",
        "slug": "eld-device-pro-fleet",
        "description": (
            "Our advanced ELD unit built for fleet operators: live GPS "
            "tracking, driver behavior reports, and fleet dashboard access "
            "included."
        ),
        "price": Decimal("219.00"),
        "discount_price": Decimal("179.00"),
        "order": 2,
    },
    {
        "title": "GPS Fleet Tracker",
        "slug": "gps-fleet-tracker",
        "description": (
            "Standalone GPS tracking unit for trailers and equipment. Real-time "
            "location updates and geofencing alerts."
        ),
        "price": Decimal("89.00"),
        "discount_price": None,
        "order": 3,
    },
]


def seed_products(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    for data in PRODUCTS:
        Product.objects.get_or_create(slug=data["slug"], defaults={**data, "is_active": True})


def remove_products(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    Product.objects.filter(slug__in=[p["slug"] for p in PRODUCTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_products, remove_products),
    ]
