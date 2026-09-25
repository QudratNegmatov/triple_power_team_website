from django.db import migrations

POINTS = [
    "Easy-to-book shipments",
    "Reliable and secure cargo handling",
    "Experienced dispatchers",
    "Full customs compliance",
    "Scalable for shipments of any size",
]

STATS = [
    {"icon": "truck", "number": "120+", "label": "Fleet vehicles"},
    {"icon": "clock", "number": "24/7", "label": "Dispatch support"},
    {"icon": "warehouse", "number": "8", "label": "Warehouses"},
    {"icon": "star", "number": "99%", "label": "On-time delivery"},
]


def seed_why_us(apps, schema_editor):
    WhyChooseUs = apps.get_model("core", "WhyChooseUs")
    WhyChooseUsPoint = apps.get_model("core", "WhyChooseUsPoint")
    WhyChooseUsStat = apps.get_model("core", "WhyChooseUsStat")

    if WhyChooseUs.objects.exists():
        return

    section = WhyChooseUs.objects.create(
        eyebrow="Why choose us",
        heading="Built for Reliable Delivery. Designed for Your Business.",
        intro=(
            "We combine a modern fleet with an experienced dispatch team "
            "that understands the logistics industry."
        ),
    )
    for order, text in enumerate(POINTS):
        WhyChooseUsPoint.objects.create(section=section, text=text, order=order)
    for order, stat in enumerate(STATS):
        WhyChooseUsStat.objects.create(section=section, order=order, **stat)


def unseed_why_us(apps, schema_editor):
    WhyChooseUs = apps.get_model("core", "WhyChooseUs")
    WhyChooseUs.objects.filter(
        heading="Built for Reliable Delivery. Designed for Your Business."
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_whychooseus_whychooseuspoint_whychooseusstat"),
    ]

    operations = [
        migrations.RunPython(seed_why_us, unseed_why_us),
    ]
