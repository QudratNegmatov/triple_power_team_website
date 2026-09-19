import datetime

from django.db import migrations
from django.utils import timezone

POSTS = [
    {
        "title": "New Warehouse Opens in the North Region",
        "slug": "new-warehouse-north-region",
        "excerpt": (
            "We have opened a new 5,000 sqm warehouse to serve clients "
            "in the north region."
        ),
        "body": (
            "We are excited to announce the opening of our newest warehouse "
            "facility, adding 5,000 square meters of secure storage capacity "
            "to better serve clients in the north region. The facility "
            "includes temperature-controlled zones and 24/7 monitoring.\n\n"
            "(Replace this with your real announcement.)"
        ),
        "days_ago": 3,
    },
    {
        "title": "Fleet Expansion: 10 New Trucks Added",
        "slug": "fleet-expansion-10-new-trucks",
        "excerpt": "Our fleet grows by 10 vehicles to support increasing delivery demand.",
        "body": (
            "To keep up with growing demand, we have added 10 new trucks to "
            "our fleet this quarter. This expansion allows us to offer more "
            "frequent routes and shorter delivery windows for our clients.\n\n"
            "(Replace this with your real announcement.)"
        ),
        "days_ago": 7,
    },
    {
        "title": "Faster Customs Clearance Process",
        "slug": "faster-customs-clearance-process",
        "excerpt": "We streamlined our customs documentation process to cut clearance times.",
        "body": (
            "We have partnered with customs authorities to streamline our "
            "documentation process, reducing average clearance times. This "
            "means faster turnaround for import and export shipments handled "
            "by our team.\n\n(Replace this with your real announcement.)"
        ),
        "days_ago": 14,
    },
]


def seed_news(apps, schema_editor):
    NewsPost = apps.get_model("news", "NewsPost")
    now = timezone.now()
    for data in POSTS:
        days_ago = data.pop("days_ago")
        NewsPost.objects.get_or_create(
            slug=data["slug"],
            defaults={
                **data,
                "published_at": now - datetime.timedelta(days=days_ago),
                "is_published": True,
            },
        )


def remove_news(apps, schema_editor):
    NewsPost = apps.get_model("news", "NewsPost")
    NewsPost.objects.filter(slug__in=[d["slug"] for d in POSTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_news, remove_news),
    ]
