from django.db import migrations

POINTS = [
    {
        "icon": "check",
        "title_en": "Easy-to-book shipments",
        "title_uz": "Yuklarni bron qilish oson",
        "title_ru": "Лёгкое бронирование грузов",
        "short_description_en": "Request a shipment in minutes through our team, no paperwork hassle.",
        "short_description_uz": "Bir necha daqiqada jamoamiz orqali yuk yuborish so'rovini yuboring.",
        "short_description_ru": "Оформите заявку на перевозку за минуты через нашу команду.",
    },
    {
        "icon": "shield",
        "title_en": "Reliable and secure cargo handling",
        "title_uz": "Ishonchli va xavfsiz yuk tashish",
        "title_ru": "Надёжная и безопасная обработка грузов",
        "short_description_en": "Your cargo is tracked and insured from pickup to delivery.",
        "short_description_uz": "Yukingiz olib ketilgan paytdan yetkazib berilguncha kuzatiladi.",
        "short_description_ru": "Ваш груз отслеживается и застрахован от забора до доставки.",
    },
    {
        "icon": "users",
        "title_en": "Experienced dispatchers",
        "title_uz": "Tajribali dispetcherlar",
        "title_ru": "Опытные диспетчеры",
        "short_description_en": "A dedicated team plans every route for speed and reliability.",
        "short_description_uz": "Maxsus jamoa har bir marshrutni tez va ishonchli rejalashtiradi.",
        "short_description_ru": "Отдельная команда планирует каждый маршрут для скорости и надёжности.",
    },
    {
        "icon": "document",
        "title_en": "Full customs compliance",
        "title_uz": "To'liq bojxona talablariga muvofiqlik",
        "title_ru": "Полное соответствие таможенным требованиям",
        "short_description_en": "All documentation is handled so your cargo clears borders on time.",
        "short_description_uz": "Barcha hujjatlar bilan shug'ullanamiz, yukingiz vaqtida chegaradan o'tadi.",
        "short_description_ru": "Мы оформляем все документы, чтобы груз вовремя прошёл границу.",
    },
    {
        "icon": "package",
        "title_en": "Scalable for shipments of any size",
        "title_uz": "Har qanday hajmdagi yuk uchun moslashuvchan",
        "title_ru": "Масштабируется под любой объём груза",
        "short_description_en": "From a single pallet to full truckloads, we handle it all.",
        "short_description_uz": "Bitta paletdan to to'liq yuk mashinasigacha — hammasini bajaramiz.",
        "short_description_ru": "От одной паллеты до полной фуры — мы справимся с любым объёмом.",
    },
]

STATS = [
    {"icon": "truck", "number": "120+", "label_en": "Fleet vehicles", "label_uz": "Avtoparkdagi mashinalar", "label_ru": "Транспортных средств"},
    {"icon": "clock", "number": "24/7", "label_en": "Dispatch support", "label_uz": "Dispetcherlik xizmati", "label_ru": "Диспетчерская поддержка"},
    {"icon": "warehouse", "number": "8", "label_en": "Warehouses", "label_uz": "Omborlar", "label_ru": "Склады"},
    {"icon": "star", "number": "99%", "label_en": "On-time delivery", "label_uz": "O'z vaqtida yetkazib berish", "label_ru": "Доставка вовремя"},
]


def seed(apps, schema_editor):
    WhyChooseUs = apps.get_model("core", "WhyChooseUs")
    WhyChooseUsPoint = apps.get_model("core", "WhyChooseUsPoint")
    WhyChooseUsStat = apps.get_model("core", "WhyChooseUsStat")

    if WhyChooseUs.objects.exists():
        return

    section = WhyChooseUs.objects.create(
        eyebrow_en="Why choose us",
        eyebrow_uz="Nega bizni tanlashadi",
        eyebrow_ru="Почему выбирают нас",
        heading_en="Built for Reliable Delivery. Designed for Your Business.",
        heading_uz="Ishonchli yetkazib berish uchun yaratilgan. Biznesingiz uchun mo'ljallangan.",
        heading_ru="Создано для надёжной доставки. Разработано для вашего бизнеса.",
        intro_en="We combine a modern fleet with an experienced dispatch team that understands the logistics industry.",
        intro_uz="Biz zamonaviy avtoparkni logistika sohasini yaxshi biladigan tajribali dispetcherlik jamoasi bilan birlashtiramiz.",
        intro_ru="Мы сочетаем современный автопарк с опытной диспетчерской командой, понимающей логистическую отрасль.",
    )
    for order, data in enumerate(POINTS):
        WhyChooseUsPoint.objects.create(section=section, order=order, **data)
    for order, data in enumerate(STATS):
        WhyChooseUsStat.objects.create(section=section, order=order, **data)


def unseed(apps, schema_editor):
    WhyChooseUs = apps.get_model("core", "WhyChooseUs")
    WhyChooseUs.objects.filter(
        heading_en="Built for Reliable Delivery. Designed for Your Business."
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
