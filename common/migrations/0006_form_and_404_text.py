"""Add SiteText rows for form field labels, the mobile menu button and the
404 page. Uses get_or_create so existing admin edits are never overwritten.
"""

from django.db import migrations

# (key, description, value_en, value_uz, value_ru)
TEXTS = [
    ("form.name", "Form field label: name", "Name", "Ismingiz", "Имя"),
    ("form.email", "Form field label: email", "Email", "Email", "Email"),
    ("form.phone", "Form field label: phone", "Phone", "Telefon", "Телефон"),
    ("form.message", "Form field label: message", "Message", "Xabar", "Сообщение"),
    ("nav.menu", "Mobile menu button (screen-reader label)", "Menu", "Menyu", "Меню"),
    ("error404.heading", "404 page heading", "Page not found", "Sahifa topilmadi", "Страница не найдена"),
    ("error404.text", "404 page text", "The page you are looking for doesn't exist or has been moved.", "Siz qidirayotgan sahifa mavjud emas yoki boshqa joyga ko'chirilgan.", "Страница, которую вы ищете, не существует или была перемещена."),
    ("error404.button", "404 page button", "Back to home", "Bosh sahifaga qaytish", "На главную"),
]


def seed(apps, schema_editor):
    SiteText = apps.get_model("common", "SiteText")
    for key, description, en, uz, ru in TEXTS:
        SiteText.objects.get_or_create(
            key=key,
            defaults={
                "description": description,
                "value_en": en,
                "value_uz": uz,
                "value_ru": ru,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0005_real_site_text"),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
