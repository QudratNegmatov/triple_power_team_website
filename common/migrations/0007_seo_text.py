"""SiteText rows for search-engine titles/descriptions and form success
messages. get_or_create: existing admin edits are kept."""

from django.db import migrations

# (key, description, value_en, value_uz, value_ru)
TEXTS = [
    (
        "seo.home_title",
        "Browser tab / Google title of the homepage (keep under ~60 characters)",
        "ELD & Dispatch Services for Trucking | Triple Power Team",
        "Trucking uchun ELD va dispatch xizmatlari | Triple Power Team",
        "ELD и диспетчерские услуги для траков | Triple Power Team",
    ),
    (
        "seo.default_description",
        "Google description of the homepage and default for other pages (~150 characters)",
        "Triple Power Team keeps US trucking companies and owner-operators compliant and loaded: ELD logs and HOS, DOT audit support, IFTA and 24/7 dispatch.",
        "Triple Power Team AQSHdagi trucking kompaniyalar va owner-operatorlar uchun: ELD loglari va HOS, DOT audit yordami, IFTA va 24/7 dispatch xizmati.",
        "Triple Power Team для траковых компаний и owner-operators в США: ELD-логи и HOS, поддержка на DOT-аудитах, IFTA и диспетчеризация 24/7.",
    ),
    (
        "seo.services_title",
        "Google title of the services page",
        "ELD, Dispatch, Safety & Fleet Services | Triple Power Team",
        "ELD, Dispatch, Safety va Fleet xizmatlari | Triple Power Team",
        "Услуги ELD, диспетчеризации, Safety и Fleet | Triple Power Team",
    ),
    (
        "seo.services_description",
        "Google description of the services page",
        "ELD service with HOS compliance and DOT audit support, plus a dispatch team that finds well-paying loads. Safety and Fleet teams are coming soon.",
        "HOS qoidalariga rioya va DOT audit yordami bilan ELD xizmati hamda yaxshi to'lanadigan yuk topadigan dispatch jamoasi. Safety va Fleet tez orada.",
        "ELD-сервис с соблюдением HOS и поддержкой на DOT-аудитах, а также диспетчеры, которые находят выгодные грузы. Safety и Fleet — скоро.",
    ),
    (
        "seo.about_description",
        "Google description of the About page",
        "Who we are: an ELD and dispatch team that has serviced 2,000+ trucks and supported 500+ companies through DOT audits. Available 24/7.",
        "Biz kimmiz: 2000+ truckka xizmat ko'rsatgan va 500+ kompaniyaga DOT auditida yordam bergan ELD va dispatch jamoasi. 24/7 aloqada.",
        "Кто мы: команда ELD и диспетчеризации — 2000+ обслуженных траков и 500+ компаний, сопровождённых на DOT-аудитах. На связи 24/7.",
    ),
    (
        "seo.news_description",
        "Google description of the News page",
        "News from Triple Power Team: ELD and HOS trainings, new services and updates for trucking companies and drivers.",
        "Triple Power Team yangiliklari: ELD va HOS bo'yicha treninglar, yangi xizmatlar va trucking kompaniyalar uchun yangiliklar.",
        "Новости Triple Power Team: тренинги по ELD и HOS, новые услуги и обновления для траковых компаний и водителей.",
    ),
    (
        "seo.products_description",
        "Google description of the Products page",
        "ELD devices and GPS trackers for trucks. Send a request and our team will help you choose and set up the right equipment.",
        "Yuk mashinalari uchun ELD qurilmalari va GPS trekerlar. So'rov yuboring — jamoamiz mos uskunani tanlash va sozlashda yordam beradi.",
        "ELD-устройства и GPS-трекеры для траков. Оставьте заявку — поможем подобрать и настроить оборудование.",
    ),
    (
        "seo.contact_description",
        "Google description of the Contact page",
        "Contact Triple Power Team: tell us how many trucks you have and which service you need. We answer 24/7.",
        "Triple Power Team bilan bog'laning: nechta truckingiz borligi va qaysi xizmat kerakligini yozing. 24/7 javob beramiz.",
        "Свяжитесь с Triple Power Team: напишите, сколько у вас траков и какая услуга нужна. Отвечаем 24/7.",
    ),
    (
        "contact.success",
        "Message shown after the contact form is sent",
        "Thanks for reaching out! We'll get back to you soon.",
        "Rahmat! Xabaringiz qabul qilindi, tez orada siz bilan bog'lanamiz.",
        "Спасибо! Мы получили ваше сообщение и скоро свяжемся с вами.",
    ),
    (
        "products.success",
        "Message shown after a product request is sent",
        "Thanks! We received your request and will contact you soon.",
        "Rahmat! So'rovingiz qabul qilindi, tez orada bog'lanamiz.",
        "Спасибо! Мы получили вашу заявку и скоро свяжемся с вами.",
    ),
    (
        "form.too_many",
        "Error when someone sends forms too often",
        "Too many messages in a short time. Please try again in a few minutes.",
        "Qisqa vaqtda juda ko'p xabar yuborildi. Bir necha daqiqadan keyin qayta urinib ko'ring.",
        "Слишком много сообщений за короткое время. Попробуйте снова через несколько минут.",
    ),
]


def seed(apps, schema_editor):
    SiteText = apps.get_model("common", "SiteText")
    for key, description, en, uz, ru in TEXTS:
        SiteText.objects.get_or_create(
            key=key,
            defaults={"description": description, "value_en": en, "value_uz": uz, "value_ru": ru},
        )


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0006_form_and_404_text"),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
