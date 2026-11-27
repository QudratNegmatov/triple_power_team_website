"""Monthly plans: "Per month" -> "Per month per truck" (only if the admin
has not changed that text)."""

from django.db import migrations


def forwards(apps, schema_editor):
    SiteText = apps.get_model("common", "SiteText")
    SiteText.objects.filter(key="pricing.period_month", value_en="Per month").update(
        value_en="Per month per truck",
        value_uz="Bir truck uchun oyiga",
        value_ru="В месяц за один трак",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("prices", "0004_seed_eld_basic_plan"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
