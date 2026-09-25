from django.db import migrations

SERVICES = [
    {
        "title_en": "Freight & Trucking",
        "title_uz": "Yuk tashish va avtotransport",
        "title_ru": "Грузоперевозки и автотранспорт",
        "short_name_en": "Reliable road freight, on time, every time.",
        "short_name_uz": "Ishonchli avtomobil yuk tashish, har doim o'z vaqtida.",
        "short_name_ru": "Надёжные автоперевозки, всегда вовремя.",
        "full_info_en": "<p>We move your cargo by road with a modern fleet and real-time tracking, covering local and long-haul routes.</p>",
        "full_info_uz": "<p>Yukingizni zamonaviy avtopark va real vaqtda kuzatish tizimi bilan mahalliy va uzoq masofali yo'nalishlarda tashiymiz.</p>",
        "full_info_ru": "<p>Мы перевозим ваш груз современным автопарком с отслеживанием в реальном времени по местным и дальним маршрутам.</p>",
        "key_points_en": "Local and long-haul routes\nReal-time GPS tracking on every load\nModern, well-maintained fleet",
        "key_points_uz": "Mahalliy va uzoq masofali yo'nalishlar\nHar bir yuk uchun real vaqtda GPS kuzatuvi\nZamonaviy, yaxshi holatdagi avtopark",
        "key_points_ru": "Местные и дальние маршруты\nGPS-отслеживание каждого груза в реальном времени\nСовременный, ухоженный автопарк",
        "icon": "truck",
        "order": 1,
    },
    {
        "title_en": "Warehousing & Storage",
        "title_uz": "Omborxona va saqlash",
        "title_ru": "Складирование и хранение",
        "short_name_en": "Secure storage with flexible short and long-term space.",
        "short_name_uz": "Qisqa va uzoq muddatli moslashuvchan xavfsiz saqlash.",
        "short_name_ru": "Безопасное хранение с гибкими сроками — от краткосрочного до долгосрочного.",
        "full_info_en": "<p>Our warehouses offer secure, climate-aware storage with inventory management so your goods are always accounted for.</p>",
        "full_info_uz": "<p>Omborlarimiz xavfsiz, iqlim nazorati bilan saqlash va inventarizatsiyani boshqarishni taklif etadi.</p>",
        "full_info_ru": "<p>Наши склады предлагают безопасное хранение с контролем климата и учётом товаров.</p>",
        "key_points_en": "Secure, monitored facilities\nShort-term and long-term storage options\nLive inventory management",
        "key_points_uz": "Xavfsiz, kuzatiladigan binolar\nQisqa va uzoq muddatli saqlash imkoniyatlari\nJonli inventarizatsiya boshqaruvi",
        "key_points_ru": "Безопасные, охраняемые объекты\nКраткосрочное и долгосрочное хранение\nУчёт товаров в реальном времени",
        "icon": "warehouse",
        "order": 2,
    },
    {
        "title_en": "Customs & Documentation",
        "title_uz": "Bojxona va hujjatlar",
        "title_ru": "Таможня и документация",
        "short_name_en": "Paperwork and customs clearance handled for you.",
        "short_name_uz": "Hujjatlar va bojxona rasmiylashtiruvi siz uchun bajariladi.",
        "short_name_ru": "Оформление документов и таможенная очистка на нас.",
        "full_info_en": "<p>We handle customs clearance and shipping documentation so your cargo crosses borders without delays.</p>",
        "full_info_uz": "<p>Biz bojxona rasmiylashtiruvi va tashish hujjatlari bilan shug'ullanamiz, shunda yukingiz kechikishsiz chegaradan o'tadi.</p>",
        "full_info_ru": "<p>Мы занимаемся таможенным оформлением и документами, чтобы груз без задержек пересекал границы.</p>",
        "key_points_en": "Full import/export documentation handled\nExperienced customs clearance team\nFewer delays at the border",
        "key_points_uz": "To'liq import/eksport hujjatlari bilan ishlash\nTajribali bojxona rasmiylashtiruvi jamoasi\nChegarada kamroq kechikishlar",
        "key_points_ru": "Полное оформление импорта/экспорта\nОпытная команда по таможенной очистке\nМеньше задержек на границе",
        "icon": "document",
        "order": 3,
    },
    {
        "title_en": "Fleet Tracking",
        "title_uz": "Avtoparkni kuzatish",
        "title_ru": "Отслеживание автопарка",
        "short_name_en": "Live GPS tracking and ETAs for every shipment.",
        "short_name_uz": "Har bir yuk uchun jonli GPS kuzatuvi va yetib borish vaqti.",
        "short_name_ru": "GPS-отслеживание и расчётное время прибытия для каждой поставки.",
        "full_info_en": "<p>Track every vehicle in real time and share accurate ETAs with your customers from pickup to final delivery.</p>",
        "full_info_uz": "<p>Har bir mashinani real vaqtda kuzating va mijozlaringizga aniq yetib borish vaqtini taqdim eting.</p>",
        "full_info_ru": "<p>Отслеживайте каждый автомобиль в реальном времени и сообщайте клиентам точное время прибытия.</p>",
        "key_points_en": "Live GPS location for every vehicle\nAccurate ETAs shared with your customers\nDelivery history and reporting",
        "key_points_uz": "Har bir mashina uchun jonli GPS joylashuvi\nMijozlar bilan aniq yetib borish vaqtini bo'lishish\nYetkazib berish tarixi va hisobotlari",
        "key_points_ru": "GPS-местоположение каждого автомобиля в реальном времени\nТочное время прибытия для клиентов\nИстория доставок и отчётность",
        "icon": "map-pin",
        "order": 4,
    },
]


def seed(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    for data in SERVICES:
        Service.objects.create(**data)


def unseed(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    Service.objects.filter(title_en__in=[s["title_en"] for s in SERVICES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
