"""Hide the demo logistics projects (warehousing, cold chain, customs) - they
don't describe Triple Power Team's real work. Real projects can be added from
the admin."""

from django.db import migrations

OLD_DEMO_TITLES = [
    "Nationwide Retail Distribution",
    "Cold Chain Expansion",
    "Port-to-Door Import Program",
]


def hide(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    Project.objects.filter(title_en__in=OLD_DEMO_TITLES).update(is_active=False)


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0002_seed_projects"),
    ]

    operations = [
        migrations.RunPython(hide, migrations.RunPython.noop),
    ]
