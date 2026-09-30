"""Replace the demo logistics services with Triple Power Team's real ones:
ELD, Dispatch (both live) and Safety, Fleet (coming soon), plus the ELD
systems we work in and the platforms we integrate with.
"""

from django.db import migrations

OLD_DEMO_TITLES = [
    "Freight & Trucking",
    "Warehousing & Storage",
    "Customs & Documentation",
    "Fleet Tracking",
]

ELD = {
    "title_en": "ELD Service",
    "title_uz": "ELD xizmati",
    "title_ru": "ELD-сервис",
    "short_name_en": "Logs, HOS compliance and audit support for your trucks — 24/7.",
    "short_name_uz": "Yuk mashinalaringiz uchun loglar, HOS qoidalariga rioya va audit yordami — 24/7.",
    "short_name_ru": "Логи, соблюдение HOS и поддержка при аудитах для ваших траков — 24/7.",
    "full_info_en": (
        "<p>ELD (Electronic Logging Device) is our core service. We take care of your drivers' "
        "logs and hours of service so your trucks stay on the road and your company stays "
        "compliant. Our team has serviced <strong>2,000+ trucks</strong> and provided audit "
        "support to <strong>500+ companies</strong>.</p>"
        "<h3>What we do</h3>"
        "<ul>"
        "<li>Monitor and manage drivers' logs and hours of service (HOS) around the clock</li>"
        "<li>Fix log errors and violations according to FMCSA rules, and plan drivers' available time</li>"
        "<li>Prepare documents and support your company through DOT audits</li>"
        "<li>IFTA — fuel tax agreements and quarterly reports</li>"
        "<li>Weekly trainings for drivers and staff on ELD and HOS rules</li>"
        "<li>Connect your ELD with Highway, Trucking Tools and other platforms</li>"
        "</ul>"
        "<h3>ELD systems we work with</h3>"
        "<p>PandaELD, UzbPrime ELD, BST ELD, Vitality ELD and many other ELD providers. "
        "If you use a different system, contact us — most likely we already work with it.</p>"
        "<h3>Your data is safe with us</h3>"
        "<p>Your company's interests always come first. Access to your ELD accounts and "
        "driver data is limited to the team working on your account and is never shared "
        "with third parties.</p>"
    ),
    "full_info_uz": (
        "<p>ELD (Electronic Logging Device — elektron jurnal qurilmasi) bizning asosiy "
        "xizmatimiz. Haydovchilaringizning loglari va ish vaqtini (HOS) biz nazorat qilamiz — "
        "yuk mashinalaringiz yo'lda, kompaniyangiz esa qoidalarga muvofiq bo'ladi. Jamoamiz "
        "<strong>2000+ yuk mashinasiga</strong> xizmat ko'rsatgan va <strong>500+ kompaniyaga</strong> "
        "audit bo'yicha yordam bergan.</p>"
        "<h3>Nimalar qilamiz</h3>"
        "<ul>"
        "<li>Haydovchilar loglari va ish vaqtini (HOS) kechayu kunduz kuzatib boramiz</li>"
        "<li>FMCSA qoidalari asosida log xatolari va buzilishlarni tuzatamiz, haydovchilarga vaqt rejalashtirib beramiz</li>"
        "<li>DOT auditlari uchun hujjatlarni tayyorlaymiz va kompaniyangizni audit davomida qo'llab-quvvatlaymiz</li>"
        "<li>IFTA — yoqilg'i solig'i bo'yicha shartnomalar va choraklik hisobotlar</li>"
        "<li>Haydovchilar va xodimlar uchun ELD va HOS qoidalari bo'yicha haftalik treninglar</li>"
        "<li>ELD tizimingizni Highway, Trucking Tools va boshqa platformalar bilan bog'laymiz</li>"
        "</ul>"
        "<h3>Biz ishlaydigan ELD tizimlari</h3>"
        "<p>PandaELD, UzbPrime ELD, BST ELD, Vitality ELD va boshqa ko'plab ELD tizimlari. "
        "Agar siz boshqa tizimdan foydalansangiz, biz bilan bog'laning — katta ehtimol bilan "
        "biz u bilan ham ishlaymiz.</p>"
        "<h3>Ma'lumotlaringiz xavfsiz</h3>"
        "<p>Kompaniyangiz manfaatlari biz uchun eng asosiy o'rinda turadi. ELD akkauntlaringiz "
        "va haydovchilar ma'lumotlariga faqat sizning akkauntingiz bilan ishlaydigan jamoa kira "
        "oladi va ular hech qachon uchinchi shaxslarga berilmaydi.</p>"
    ),
    "full_info_ru": (
        "<p>ELD (Electronic Logging Device — электронный бортовой журнал) — наш основной "
        "сервис. Мы ведём логи и часы работы (HOS) ваших водителей, чтобы траки оставались "
        "в пути, а компания — в соответствии с требованиями. Наша команда обслужила "
        "<strong>2000+ траков</strong> и оказала поддержку при аудитах <strong>500+ компаниям</strong>.</p>"
        "<h3>Что мы делаем</h3>"
        "<ul>"
        "<li>Круглосуточно контролируем логи и часы работы (HOS) водителей</li>"
        "<li>Исправляем ошибки и нарушения в логах по правилам FMCSA и планируем доступное время водителей</li>"
        "<li>Готовим документы и сопровождаем компанию во время DOT-аудитов</li>"
        "<li>IFTA — соглашения по топливному налогу и ежеквартальные отчёты</li>"
        "<li>Еженедельные тренинги по правилам ELD и HOS для водителей и сотрудников</li>"
        "<li>Подключаем ваш ELD к Highway, Trucking Tools и другим платформам</li>"
        "</ul>"
        "<h3>ELD-системы, с которыми мы работаем</h3>"
        "<p>PandaELD, UzbPrime ELD, BST ELD, Vitality ELD и многие другие ELD-системы. "
        "Если вы пользуетесь другой системой — свяжитесь с нами, скорее всего, мы с ней "
        "уже работаем.</p>"
        "<h3>Ваши данные в безопасности</h3>"
        "<p>Интересы вашей компании для нас всегда на первом месте. Доступ к вашим "
        "ELD-аккаунтам и данным водителей есть только у команды, которая работает с вашим "
        "аккаунтом, и они никогда не передаются третьим лицам.</p>"
    ),
    "key_points_en": (
        "2,000+ trucks serviced\n"
        "Audit support for 500+ companies\n"
        "24/7 support\n"
        "Weekly trainings\n"
        "IFTA agreements and reports\n"
        "Integrations with Highway, Trucking Tools and more"
    ),
    "key_points_uz": (
        "2000+ yuk mashinasiga xizmat ko'rsatilgan\n"
        "500+ kompaniya uchun audit yordami\n"
        "24/7 xizmat\n"
        "Haftalik treninglar\n"
        "IFTA shartnomalari va hisobotlari\n"
        "Highway, Trucking Tools va boshqa tizimlar bilan integratsiya"
    ),
    "key_points_ru": (
        "Обслужено 2000+ траков\n"
        "Поддержка при аудитах для 500+ компаний\n"
        "Поддержка 24/7\n"
        "Еженедельные тренинги\n"
        "IFTA: соглашения и отчёты\n"
        "Интеграции с Highway, Trucking Tools и другими системами"
    ),
    "icon": "clock",
    "is_coming_soon": False,
    "order": 1,
}

DISPATCH = {
    "title_en": "Dispatch Team",
    "title_uz": "Dispatch jamoasi",
    "title_ru": "Диспетчерская команда",
    "short_name_en": "We find loads, talk to brokers and stay with your driver until delivery.",
    "short_name_uz": "Yuk topamiz, brokerlar bilan gaplashamiz va yuk topshirilguncha haydovchi bilan birga bo'lamiz.",
    "short_name_ru": "Находим грузы, ведём переговоры с брокерами и сопровождаем водителя до доставки.",
    "full_info_en": (
        "<p>Our dispatch team keeps your trucks loaded and your drivers informed. We handle "
        "the whole trip — from finding the load to the moment it is delivered — so owners "
        "and drivers can focus on driving.</p>"
        "<h3>What we do</h3>"
        "<ul>"
        "<li><strong>Find loads</strong> — we search for well-paying loads that fit your truck, lanes and schedule</li>"
        "<li><strong>Work with brokers</strong> — rate negotiation, rate confirmations and all communication</li>"
        "<li><strong>Explain the route</strong> — we plan the route and walk the driver through pickup and delivery details</li>"
        "<li><strong>Deliver the load</strong> — we coordinate pickup, delivery and the paperwork (BOL, POD) until the load is handed over</li>"
        "<li><strong>Constant contact with the driver</strong> — our dispatchers are reachable during the whole trip</li>"
        "<li><strong>Active loads</strong> — we track every active load and update the broker and your company on its status</li>"
        "</ul>"
        "<p>Your company's interests always come first: we choose loads that are profitable "
        "for you, and your company and load information stays confidential.</p>"
    ),
    "full_info_uz": (
        "<p>Dispatch jamoamiz yuk mashinalaringiz bo'sh turmasligi va haydovchilaringiz doim "
        "xabardor bo'lishi uchun ishlaydi. Yukni topishdan tortib uni topshirgunga qadar "
        "butun reysni biz boshqaramiz — truck egalari va haydovchilar esa faqat yo'lga "
        "e'tibor beradi.</p>"
        "<h3>Nimalar qilamiz</h3>"
        "<ul>"
        "<li><strong>Driver uchun yuk topish</strong> — yuk mashinangiz, yo'nalishlaringiz va jadvalingizga mos, yaxshi to'lanadigan yuklarni qidiramiz</li>"
        "<li><strong>Broker bilan aloqa</strong> — narx bo'yicha kelishuv, rate confirmation va barcha muloqot</li>"
        "<li><strong>Driverga yo'lni tushuntirish</strong> — marshrutni rejalashtiramiz, pickup va delivery tafsilotlarini haydovchiga tushuntiramiz</li>"
        "<li><strong>Yukni topshirish</strong> — yuk topshirilguncha pickup, delivery va hujjatlarni (BOL, POD) nazorat qilamiz</li>"
        "<li><strong>Driver bilan doimiy aloqa</strong> — dispetcherlarimiz butun reys davomida aloqada</li>"
        "<li><strong>Faol yuklar</strong> — har bir faol yukni kuzatamiz, broker va kompaniyangizga holati haqida xabar beramiz</li>"
        "</ul>"
        "<p>Kompaniyangiz manfaatlari eng asosiy o'rinda: siz uchun foydali yuklarni tanlaymiz, "
        "kompaniya va yuklar haqidagi ma'lumotlar esa sir saqlanadi.</p>"
    ),
    "full_info_ru": (
        "<p>Наша диспетчерская команда следит за тем, чтобы ваши траки не простаивали, а "
        "водители всегда были в курсе. Мы ведём весь рейс — от поиска груза до его "
        "сдачи, — чтобы владельцы и водители могли сосредоточиться на дороге.</p>"
        "<h3>Что мы делаем</h3>"
        "<ul>"
        "<li><strong>Поиск грузов</strong> — ищем хорошо оплачиваемые грузы под ваш трак, направления и график</li>"
        "<li><strong>Работа с брокерами</strong> — переговоры по ставке, rate confirmation и вся коммуникация</li>"
        "<li><strong>Объясняем маршрут</strong> — планируем маршрут и разъясняем водителю детали погрузки и выгрузки</li>"
        "<li><strong>Сдача груза</strong> — контролируем погрузку, доставку и документы (BOL, POD) до сдачи груза</li>"
        "<li><strong>Постоянная связь с водителем</strong> — наши диспетчеры на связи весь рейс</li>"
        "<li><strong>Активные грузы</strong> — отслеживаем каждый активный груз и сообщаем брокеру и вашей компании его статус</li>"
        "</ul>"
        "<p>Интересы вашей компании всегда на первом месте: мы выбираем выгодные для вас "
        "грузы, а информация о компании и грузах остаётся конфиденциальной.</p>"
    ),
    "key_points_en": (
        "Finding loads for your drivers\n"
        "Communication with brokers\n"
        "Route explained to the driver\n"
        "Load delivery and paperwork\n"
        "Constant contact with the driver\n"
        "Tracking of all active loads"
    ),
    "key_points_uz": (
        "Driver uchun yuk topish\n"
        "Broker bilan aloqa\n"
        "Driverga yo'lni tushuntirish\n"
        "Yukni topshirish va hujjatlar\n"
        "Driver bilan doimiy aloqa\n"
        "Barcha faol yuklarni kuzatish"
    ),
    "key_points_ru": (
        "Поиск грузов для водителей\n"
        "Связь с брокерами\n"
        "Объяснение маршрута водителю\n"
        "Сдача груза и документы\n"
        "Постоянная связь с водителем\n"
        "Контроль всех активных грузов"
    ),
    "icon": "map-pin",
    "is_coming_soon": False,
    "order": 2,
}

SAFETY = {
    "title_en": "Safety Team",
    "title_uz": "Safety jamoasi",
    "title_ru": "Отдел безопасности (Safety)",
    "short_name_en": "DOT compliance, driver files and safety support for your company.",
    "short_name_uz": "Kompaniyangiz uchun DOT talablariga muvofiqlik, haydovchi hujjatlari va xavfsizlik bo'yicha yordam.",
    "short_name_ru": "Соответствие требованиям DOT, документы водителей и поддержка по безопасности.",
    "full_info_en": (
        "<p><strong>Coming soon.</strong> We are preparing our Safety team so we can take "
        "care of your company's compliance in one place, together with ELD and dispatch.</p>"
        "<h3>What the Safety team will do</h3>"
        "<ul>"
        "<li>Keep your company compliant with FMCSA and DOT requirements</li>"
        "<li>Build and maintain driver qualification files (DQ files)</li>"
        "<li>Manage drug & alcohol testing program requirements</li>"
        "<li>Monitor your CSA scores and handle roadside inspection reports</li>"
        "<li>Prepare your company for DOT audits and new-entrant safety audits</li>"
        "<li>Support accidents and insurance claims</li>"
        "<li>Run safety trainings for drivers</li>"
        "</ul>"
        "<p>Want to be among the first clients? Contact us and we'll let you know as soon as it launches.</p>"
    ),
    "full_info_uz": (
        "<p><strong>Tez orada.</strong> Biz Safety jamoamizni tayyorlayapmiz — shunda "
        "kompaniyangizning qoidalarga muvofiqligini ELD va dispatch bilan birga bir joyda "
        "nazorat qila olamiz.</p>"
        "<h3>Safety jamoasi nimalar qiladi</h3>"
        "<ul>"
        "<li>Kompaniyangizni FMCSA va DOT talablariga muvofiq holda ushlab turish</li>"
        "<li>Haydovchilarning malaka hujjatlarini (DQ file) tayyorlash va yuritish</li>"
        "<li>Drug & alcohol test dasturi talablarini boshqarish</li>"
        "<li>CSA ballaringizni kuzatish va yo'ldagi inspeksiya hisobotlari bilan ishlash</li>"
        "<li>Kompaniyangizni DOT auditlari va new-entrant auditiga tayyorlash</li>"
        "<li>Avariyalar va sug'urta da'volari bo'yicha yordam</li>"
        "<li>Haydovchilar uchun xavfsizlik treninglari</li>"
        "</ul>"
        "<p>Birinchi mijozlardan bo'lishni xohlaysizmi? Biz bilan bog'laning — ishga tushishi bilan xabar beramiz.</p>"
    ),
    "full_info_ru": (
        "<p><strong>Скоро.</strong> Мы готовим отдел Safety, чтобы вести соответствие вашей "
        "компании требованиям в одном месте — вместе с ELD и диспетчерской службой.</p>"
        "<h3>Чем будет заниматься отдел Safety</h3>"
        "<ul>"
        "<li>Поддержание соответствия компании требованиям FMCSA и DOT</li>"
        "<li>Оформление и ведение квалификационных файлов водителей (DQ files)</li>"
        "<li>Сопровождение программы тестирования на наркотики и алкоголь</li>"
        "<li>Контроль CSA-баллов и работа с отчётами о дорожных инспекциях</li>"
        "<li>Подготовка компании к DOT-аудитам и new-entrant аудиту</li>"
        "<li>Сопровождение ДТП и страховых случаев</li>"
        "<li>Тренинги по безопасности для водителей</li>"
        "</ul>"
        "<p>Хотите стать одним из первых клиентов? Свяжитесь с нами — сообщим сразу после запуска.</p>"
    ),
    "key_points_en": "FMCSA / DOT compliance\nDriver qualification files\nCSA score monitoring\nAudit preparation",
    "key_points_uz": "FMCSA / DOT talablariga muvofiqlik\nHaydovchi malaka hujjatlari\nCSA ballarini kuzatish\nAuditga tayyorlash",
    "key_points_ru": "Соответствие FMCSA / DOT\nКвалификационные файлы водителей\nКонтроль CSA-баллов\nПодготовка к аудитам",
    "icon": "shield",
    "is_coming_soon": True,
    "order": 3,
}

FLEET = {
    "title_en": "Fleet Team",
    "title_uz": "Fleet jamoasi",
    "title_ru": "Отдел автопарка (Fleet)",
    "short_name_en": "Maintenance, repairs and paperwork for your trucks and trailers.",
    "short_name_uz": "Yuk mashinalari va treylerlaringiz uchun texnik xizmat, ta'mirlash va hujjatlar.",
    "short_name_ru": "Обслуживание, ремонт и документы для ваших траков и трейлеров.",
    "full_info_en": (
        "<p><strong>Coming soon.</strong> Our Fleet team will help you keep every truck "
        "and trailer in working order, so your equipment earns money instead of standing "
        "in the shop.</p>"
        "<h3>What the Fleet team will do</h3>"
        "<ul>"
        "<li>Plan preventive maintenance and keep service history for every unit</li>"
        "<li>Find repair shops and roadside assistance when a truck breaks down</li>"
        "<li>Track registrations, permits, inspections and their expiry dates</li>"
        "<li>Manage fuel cards and tolls</li>"
        "<li>Track truck locations and equipment status</li>"
        "<li>Prepare expense reports for your fleet</li>"
        "</ul>"
        "<p>Want to be among the first clients? Contact us and we'll let you know as soon as it launches.</p>"
    ),
    "full_info_uz": (
        "<p><strong>Tez orada.</strong> Fleet jamoamiz har bir yuk mashinasi va treyleringizni "
        "ishchi holatda ushlashga yordam beradi — texnikangiz ustaxonada turmasdan, pul "
        "ishlab topadi.</p>"
        "<h3>Fleet jamoasi nimalar qiladi</h3>"
        "<ul>"
        "<li>Profilaktik texnik xizmatni rejalashtirish va har bir mashina tarixini yuritish</li>"
        "<li>Mashina buzilganda ustaxona va yo'l yordamini topish</li>"
        "<li>Registratsiya, ruxsatnomalar, inspeksiyalar va ularning muddatlarini kuzatish</li>"
        "<li>Yoqilg'i kartalari va toll to'lovlarini boshqarish</li>"
        "<li>Mashinalar joylashuvi va texnika holatini kuzatish</li>"
        "<li>Avtopark bo'yicha xarajatlar hisobotlarini tayyorlash</li>"
        "</ul>"
        "<p>Birinchi mijozlardan bo'lishni xohlaysizmi? Biz bilan bog'laning — ishga tushishi bilan xabar beramiz.</p>"
    ),
    "full_info_ru": (
        "<p><strong>Скоро.</strong> Отдел Fleet поможет держать каждый трак и трейлер в "
        "рабочем состоянии, чтобы техника зарабатывала, а не простаивала в ремонте.</p>"
        "<h3>Чем будет заниматься отдел Fleet</h3>"
        "<ul>"
        "<li>Планирование профилактического обслуживания и история сервиса по каждой единице</li>"
        "<li>Поиск ремонтных мастерских и помощи на дороге при поломке</li>"
        "<li>Контроль регистраций, разрешений, инспекций и сроков их действия</li>"
        "<li>Управление топливными картами и платными дорогами</li>"
        "<li>Отслеживание местоположения траков и состояния техники</li>"
        "<li>Отчёты по расходам автопарка</li>"
        "</ul>"
        "<p>Хотите стать одним из первых клиентов? Свяжитесь с нами — сообщим сразу после запуска.</p>"
    ),
    "key_points_en": "Preventive maintenance\nRepairs and roadside assistance\nPermits and registrations\nFuel cards and tolls",
    "key_points_uz": "Profilaktik texnik xizmat\nTa'mirlash va yo'l yordami\nRuxsatnomalar va registratsiya\nYoqilg'i kartalari va toll to'lovlari",
    "key_points_ru": "Профилактическое обслуживание\nРемонт и помощь на дороге\nРазрешения и регистрации\nТопливные карты и платные дороги",
    "icon": "truck",
    "is_coming_soon": True,
    "order": 4,
}

SERVICES = [ELD, DISPATCH, SAFETY, FLEET]

# Brand names aren't translated. Links left blank can be filled in from the admin.
ELD_USED_SYSTEMS = [
    {"name": "PandaELD", "order": 1},
    {"name": "UzbPrime ELD", "order": 2},
    {"name": "BST ELD", "order": 3},
    {"name": "Vitality ELD", "order": 4},
]

ELD_INTEGRATED_SYSTEMS = [
    {"name": "Highway", "link": "https://www.highway.com/", "order": 1},
    {"name": "Trucking Tools", "link": "https://truckingtools.com/", "order": 2},
]


def seed(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    UsedSystem = apps.get_model("services", "UsedSystem")
    IntegratedSystem = apps.get_model("services", "IntegratedSystem")

    Service.objects.filter(title_en__in=OLD_DEMO_TITLES).delete()

    services = {}
    for data in SERVICES:
        data = dict(data)
        title_en = data.pop("title_en")
        service, _ = Service.objects.update_or_create(title_en=title_en, defaults={**data, "is_active": True})
        services[title_en] = service

    eld = services[ELD["title_en"]]
    for data in ELD_USED_SYSTEMS:
        UsedSystem.objects.get_or_create(service=eld, name=data["name"], defaults=data)
    for data in ELD_INTEGRATED_SYSTEMS:
        IntegratedSystem.objects.get_or_create(service=eld, name=data["name"], defaults=data)


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0005_service_is_coming_soon"),
        ("prices", "0002_seed_prices"),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
