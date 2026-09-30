"""Replace the demo logistics copy in the Why Choose Us section and the About
page with Triple Power Team's real business (ELD and dispatch services), and
hide the placeholder testimonials so no made-up client quotes are shown.
"""

from django.db import migrations

WHY_US = {
    "eyebrow_en": "Why choose us",
    "eyebrow_uz": "Nega bizni tanlashadi",
    "eyebrow_ru": "Почему выбирают нас",
    "heading_en": "Your Company's Interests Come First",
    "heading_uz": "Kompaniyangiz manfaatlari birinchi o'rinda",
    "heading_ru": "Интересы вашей компании — на первом месте",
    "intro_en": "We work as part of your team: we keep your trucks compliant and loaded, and we protect your company's data as our own.",
    "intro_uz": "Biz sizning jamoangizning bir qismi sifatida ishlaymiz: mashinalaringizni qoidalarga muvofiq va yukli holda ushlaymiz, kompaniyangiz ma'lumotlarini o'zimiznikidek himoya qilamiz.",
    "intro_ru": "Мы работаем как часть вашей команды: держим траки в соответствии с правилами и с грузом, а данные вашей компании защищаем как свои.",
}

POINTS = [
    {
        "icon": "clock",
        "title_en": "24/7 support",
        "title_uz": "24/7 xizmat",
        "title_ru": "Поддержка 24/7",
        "short_description_en": "Our team is available day and night, weekends and holidays included.",
        "short_description_uz": "Jamoamiz kechayu kunduz, dam olish va bayram kunlari ham aloqada.",
        "short_description_ru": "Наша команда на связи днём и ночью, включая выходные и праздники.",
    },
    {
        "icon": "document",
        "title_en": "Audit support",
        "title_uz": "Audit yordami",
        "title_ru": "Поддержка при аудитах",
        "short_description_en": "We have prepared and supported 500+ companies through DOT audits.",
        "short_description_uz": "500+ kompaniyani DOT auditlariga tayyorlaganmiz va audit davomida yordam berganmiz.",
        "short_description_ru": "Мы подготовили и сопроводили на DOT-аудитах более 500 компаний.",
    },
    {
        "icon": "users",
        "title_en": "Weekly trainings",
        "title_uz": "Haftalik treninglar",
        "title_ru": "Еженедельные тренинги",
        "short_description_en": "Regular trainings for drivers and staff on ELD and HOS rules.",
        "short_description_uz": "Haydovchilar va xodimlar uchun ELD va HOS qoidalari bo'yicha muntazam treninglar.",
        "short_description_ru": "Регулярные тренинги по правилам ELD и HOS для водителей и сотрудников.",
    },
    {
        "icon": "globe",
        "title_en": "Connected to your systems",
        "title_uz": "Tizimlaringiz bilan bog'langan",
        "title_ru": "Связь с вашими системами",
        "short_description_en": "PandaELD, UzbPrime ELD, BST ELD, Vitality ELD and more — plus Highway and Trucking Tools.",
        "short_description_uz": "PandaELD, UzbPrime ELD, BST ELD, Vitality ELD va boshqalar — hamda Highway va Trucking Tools.",
        "short_description_ru": "PandaELD, UzbPrime ELD, BST ELD, Vitality ELD и другие — а также Highway и Trucking Tools.",
    },
    {
        "icon": "package",
        "title_en": "IFTA agreements",
        "title_uz": "IFTA shartnomalari",
        "title_ru": "Соглашения IFTA",
        "short_description_en": "We handle IFTA fuel tax paperwork and quarterly reports.",
        "short_description_uz": "IFTA yoqilg'i solig'i hujjatlari va choraklik hisobotlarini tayyorlaymiz.",
        "short_description_ru": "Ведём документы по топливному налогу IFTA и ежеквартальные отчёты.",
    },
    {
        "icon": "shield",
        "title_en": "Your data is protected",
        "title_uz": "Ma'lumotlaringiz himoyalangan",
        "title_ru": "Ваши данные под защитой",
        "short_description_en": "Access to your accounts is strictly limited and your data is never shared with third parties.",
        "short_description_uz": "Akkauntlaringizga kirish qat'iy cheklangan, ma'lumotlaringiz hech qachon uchinchi shaxslarga berilmaydi.",
        "short_description_ru": "Доступ к вашим аккаунтам строго ограничен, данные никогда не передаются третьим лицам.",
    },
]

STATS = [
    {"icon": "truck", "number": "2000+", "label_en": "Trucks serviced", "label_uz": "Xizmat ko'rsatilgan truck", "label_ru": "Обслуженных траков"},
    {"icon": "document", "number": "500+", "label_en": "Companies with audit support", "label_uz": "Kompaniyaga audit yordami", "label_ru": "Компаний с поддержкой аудита"},
    {"icon": "clock", "number": "24/7", "label_en": "Support", "label_uz": "Xizmat", "label_ru": "Поддержка"},
    {"icon": "dashboard", "number": "4+", "label_en": "ELD systems", "label_uz": "ELD tizimlari", "label_ru": "ELD-систем"},
]

ABOUT = {
    "title_en": "About Triple Power Team",
    "title_uz": "Triple Power Team haqida",
    "title_ru": "О Triple Power Team",
    "short_description_en": (
        "We are a service company for trucking companies and owner-operators. Our ELD team "
        "has serviced 2,000+ trucks and supported 500+ companies through audits, and our "
        "dispatchers keep drivers loaded and informed."
    ),
    "short_description_uz": (
        "Biz trucking kompaniyalar va truck egalari uchun xizmat ko'rsatuvchi kompaniyamiz. "
        "ELD jamoamiz 2000+ truckka xizmat ko'rsatgan va 500+ kompaniyaga auditda yordam "
        "bergan, dispetcherlarimiz esa haydovchilarni yuk va ma'lumot bilan ta'minlaydi."
    ),
    "short_description_ru": (
        "Мы сервисная компания для траковых компаний и владельцев траков. Наша ELD-команда "
        "обслужила 2000+ траков и поддержала 500+ компаний на аудитах, а диспетчеры "
        "обеспечивают водителей грузами и информацией."
    ),
    "full_description_en": (
        "<p>Triple Power Team is a service company for businesses that own trucks — from "
        "trucking companies with large fleets to owner-operators with a single truck. We take "
        "over the office work behind every truck so our clients can focus on the road.</p>"
        "<h3>What we do</h3>"
        "<ul>"
        "<li><strong>ELD service</strong> — our main service. We manage logs and hours of service, "
        "support companies through DOT audits, handle IFTA paperwork and run weekly trainings. "
        "So far we have serviced 2,000+ trucks and supported 500+ companies through audits.</li>"
        "<li><strong>Dispatch team</strong> — we find loads, talk to brokers, explain the route to "
        "the driver, stay in touch during the whole trip and make sure every load is delivered.</li>"
        "<li><strong>Safety team</strong> and <strong>Fleet team</strong> — coming soon.</li>"
        "</ul>"
        "<h3>How we work</h3>"
        "<p>Your company's interests always come first. We work in the systems you already use — "
        "PandaELD, UzbPrime ELD, BST ELD, Vitality ELD and other ELDs, connected with Highway, "
        "Trucking Tools and similar platforms. We pay close attention to data security: access "
        "to your accounts is limited to the team working with you, and your information is never "
        "shared with third parties.</p>"
        "<p>Our team is available 24/7.</p>"
    ),
    "full_description_uz": (
        "<p>Triple Power Team — truck'lari bor bizneslar uchun xizmat ko'rsatuvchi kompaniya: "
        "katta avtoparkli trucking kompaniyalardan tortib bitta truck egasigacha. Har bir truck "
        "ortidagi ofis ishlarini biz o'z zimmamizga olamiz, mijozlarimiz esa yo'lga e'tibor "
        "qaratadi.</p>"
        "<h3>Nimalar qilamiz</h3>"
        "<ul>"
        "<li><strong>ELD xizmati</strong> — asosiy xizmatimiz. Loglar va ish vaqtini (HOS) boshqaramiz, "
        "kompaniyalarga DOT auditlarida yordam beramiz, IFTA hujjatlarini yuritamiz va haftalik "
        "treninglar o'tkazamiz. Hozirgacha 2000+ truckka xizmat ko'rsatganmiz va 500+ kompaniyaga "
        "auditda yordam berganmiz.</li>"
        "<li><strong>Dispatch jamoasi</strong> — yuk topamiz, brokerlar bilan gaplashamiz, driverga "
        "yo'lni tushuntiramiz, butun reys davomida aloqada bo'lamiz va har bir yuk topshirilishini "
        "nazorat qilamiz.</li>"
        "<li><strong>Safety jamoasi</strong> va <strong>Fleet jamoasi</strong> — tez orada.</li>"
        "</ul>"
        "<h3>Qanday ishlaymiz</h3>"
        "<p>Kompaniyangiz manfaatlari biz uchun eng asosiy o'rinda turadi. Biz siz allaqachon "
        "foydalanayotgan tizimlarda ishlaymiz — PandaELD, UzbPrime ELD, BST ELD, Vitality ELD va "
        "boshqa ELD'lar, Highway, Trucking Tools va shunga o'xshash platformalar bilan bog'langan "
        "holda. Ma'lumotlar xavfsizligiga katta e'tibor beramiz: akkauntlaringizga faqat siz bilan "
        "ishlaydigan jamoa kira oladi va ma'lumotlaringiz hech qachon uchinchi shaxslarga "
        "berilmaydi.</p>"
        "<p>Jamoamiz 24/7 aloqada.</p>"
    ),
    "full_description_ru": (
        "<p>Triple Power Team — сервисная компания для бизнеса с траками: от траковых компаний "
        "с большим автопарком до владельцев одного трака. Мы берём на себя офисную работу за "
        "каждым траком, чтобы наши клиенты могли сосредоточиться на дороге.</p>"
        "<h3>Что мы делаем</h3>"
        "<ul>"
        "<li><strong>ELD-сервис</strong> — наша основная услуга. Ведём логи и часы работы (HOS), "
        "сопровождаем компании на DOT-аудитах, занимаемся документами IFTA и проводим "
        "еженедельные тренинги. На сегодня мы обслужили 2000+ траков и поддержали 500+ компаний "
        "на аудитах.</li>"
        "<li><strong>Диспетчерская команда</strong> — находим грузы, ведём переговоры с брокерами, "
        "объясняем водителю маршрут, остаёмся на связи весь рейс и контролируем сдачу каждого "
        "груза.</li>"
        "<li><strong>Отдел Safety</strong> и <strong>отдел Fleet</strong> — скоро.</li>"
        "</ul>"
        "<h3>Как мы работаем</h3>"
        "<p>Интересы вашей компании для нас всегда на первом месте. Мы работаем в тех системах, "
        "которыми вы уже пользуетесь, — PandaELD, UzbPrime ELD, BST ELD, Vitality ELD и других ELD, "
        "связанных с Highway, Trucking Tools и похожими платформами. Мы уделяем большое внимание "
        "безопасности данных: доступ к вашим аккаунтам есть только у команды, которая с вами "
        "работает, и ваша информация никогда не передаётся третьим лицам.</p>"
        "<p>Наша команда на связи 24/7.</p>"
    ),
    "contact_label_en": "Contact us",
    "contact_label_uz": "Biz bilan bog'laning",
    "contact_label_ru": "Свяжитесь с нами",
    "contact_url": "/contact/",
}


def seed(apps, schema_editor):
    WhyChooseUs = apps.get_model("core", "WhyChooseUs")
    WhyChooseUsPoint = apps.get_model("core", "WhyChooseUsPoint")
    WhyChooseUsStat = apps.get_model("core", "WhyChooseUsStat")
    AboutPage = apps.get_model("core", "AboutPage")
    Testimonial = apps.get_model("core", "Testimonial")

    section = WhyChooseUs.objects.filter(is_active=True).first() or WhyChooseUs.objects.first()
    if section is None:
        section = WhyChooseUs.objects.create(**WHY_US)
    else:
        for field, value in WHY_US.items():
            setattr(section, field, value)
        section.is_active = True
        section.save()
    section.points.all().delete()
    section.stats.all().delete()
    for order, data in enumerate(POINTS):
        WhyChooseUsPoint.objects.create(section=section, order=order, **data)
    for order, data in enumerate(STATS):
        WhyChooseUsStat.objects.create(section=section, order=order, **data)

    # Keep any uploaded About image; only the text is replaced.
    about = AboutPage.objects.filter(is_active=True).first() or AboutPage.objects.first()
    if about is None:
        AboutPage.objects.create(**ABOUT)
    else:
        for field, value in ABOUT.items():
            setattr(about, field, value)
        about.save()

    Testimonial.objects.filter(name="Placeholder Client").update(is_active=False)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_alter_heroslide_description_en_and_more"),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
