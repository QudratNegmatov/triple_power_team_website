"""Add a readable slug (used in page URLs instead of the UUID) and fill it
from the English title for existing rows."""

from django.db import migrations, models
from django.utils.text import slugify


def fill_slugs(apps, schema_editor):
    Model = apps.get_model("services", "Service")
    used = set()
    for obj in Model.objects.order_by("created_at"):
        base = (slugify(obj.title_en) or "item")[:110].strip("-")
        slug, n = base, 2
        while slug in used:
            slug = f"{base}-{n}"
            n += 1
        used.add(slug)
        obj.slug = slug
        obj.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0006_real_services_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="slug",
            field=models.SlugField(max_length=120, blank=True, default="", db_index=False),
            preserve_default=False,
        ),
        migrations.RunPython(fill_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="service",
            name="slug",
            field=models.SlugField(
                max_length=120,
                unique=True,
                blank=True,
                help_text='Part of the page address, e.g. "eld-service". Leave blank to fill it from the English title.',
            ),
        ),
    ]
