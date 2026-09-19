from django.db import migrations

PROJECTS = [
    {
        "title": "Nationwide Retail Distribution",
        "slug": "nationwide-retail-distribution",
        "summary": "Multi-region distribution network for a retail chain.",
        "description": (
            "Set up a distribution network across multiple regions, "
            "cutting average delivery time significantly."
        ),
        "client": "Retail Client",
        "order": 1,
    },
    {
        "title": "Cold Chain Expansion",
        "slug": "cold-chain-expansion",
        "summary": "Temperature-controlled storage and transport rollout.",
        "description": (
            "Expanded cold storage and refrigerated transport capacity "
            "for a food distributor."
        ),
        "client": "Food Distributor",
        "order": 2,
    },
    {
        "title": "Port-to-Door Import Program",
        "slug": "port-to-door-import-program",
        "summary": "End-to-end import handling from port to final delivery.",
        "description": (
            "Managed customs clearance, warehousing, and last-mile "
            "delivery for an importer."
        ),
        "client": "Import Business",
        "order": 3,
    },
]


def seed_projects(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    for data in PROJECTS:
        Project.objects.get_or_create(slug=data["slug"], defaults=data)


def remove_projects(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    Project.objects.filter(slug__in=[d["slug"] for d in PROJECTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_projects, remove_projects),
    ]
