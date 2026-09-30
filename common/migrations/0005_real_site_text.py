"""Rewrite the demo logistics copy for Triple Power Team's real business:
ELD and dispatch services for trucking companies and owner-operators.

Uses update_or_create, so existing rows are overwritten with the new copy.
"""

from django.db import migrations

# (key, description, value_en, value_uz, value_ru)
TEXTS = [
    ("marquee.item1", "Scrolling ticker word 1", "ELD Service", "ELD xizmati", "ELD-сервис"),
    ("marquee.item2", "Scrolling ticker word 2", "Dispatch", "Dispatch", "Диспетчеризация"),
    ("marquee.item3", "Scrolling ticker word 3", "HOS Compliance", "HOS qoidalariga rioya", "Соблюдение HOS"),
    ("marquee.item4", "Scrolling ticker word 4", "DOT Audit Support", "DOT audit yordami", "Поддержка DOT-аудитов"),
    ("marquee.item5", "Scrolling ticker word 5", "IFTA", "IFTA", "IFTA"),
    ("marquee.item6", "Scrolling ticker word 6", "24/7 Support", "24/7 yordam", "Поддержка 24/7"),

    ("hero.eyebrow", "Homepage hero eyebrow label", "ELD & dispatch services for trucking companies", "Trucking kompaniyalar uchun ELD va dispatch xizmatlari", "ELD и диспетчерские услуги для траковых компаний"),
    ("hero.heading", "Homepage hero headline (line break kept as-is)", "Your Trucks. Our Team.\nCompliant and Moving 24/7.", "Sizning truckingiz. Bizning jamoa.\nQoidalarga muvofiq, 24/7 harakatda.", "Ваши траки. Наша команда.\nПо правилам и в пути 24/7."),
    ("hero.lead", "Homepage hero paragraph", "Triple Power Team supports trucking companies and owner-operators: we manage ELD logs and HOS, support you through audits, and our dispatchers keep your trucks loaded.", "Triple Power Team trucking kompaniyalar va truck egalariga xizmat ko'rsatadi: ELD loglari va HOS'ni boshqaramiz, auditlarda yordam beramiz, dispetcherlarimiz esa mashinalaringizni yuksiz qoldirmaydi.", "Triple Power Team работает с траковыми компаниями и владельцами траков: ведём ELD-логи и HOS, сопровождаем на аудитах, а наши диспетчеры обеспечивают траки грузами."),
    ("hero.feature1", "Hero checklist item 1", "2,000+ trucks serviced", "2000+ truckka xizmat", "2000+ обслуженных траков"),
    ("hero.feature2", "Hero checklist item 2", "24/7 support", "24/7 xizmat", "Поддержка 24/7"),
    ("hero.feature3", "Hero checklist item 3", "Audit support", "Audit yordami", "Поддержка на аудитах"),
    ("hero.feature4", "Hero checklist item 4", "Weekly trainings", "Haftalik treninglar", "Еженедельные тренинги"),
    ("hero.cta_quote", "Button: Request a quote (used in several places)", "Get started", "Bog'lanish", "Начать работу"),
    ("hero.cta_services", "Button: See our services", "See our services", "Xizmatlarimizni ko'rish", "Посмотреть наши услуги"),

    ("services.eyebrow", "Homepage services section eyebrow", "Our services", "Xizmatlarimiz", "Наши услуги"),
    ("services.heading", "Homepage services section heading", "Everything Your Trucks Need", "Truckingiz uchun kerakli hamma narsa", "Всё, что нужно вашим тракам"),
    ("services.explore", "Button: Explore all services", "Explore all services", "Barcha xizmatlarni ko'rish", "Смотреть все услуги"),
    ("services.coming_soon", "Badge on services that aren't available yet", "Coming soon", "Tez orada", "Скоро"),
    ("services.coming_soon_note", "Service detail page: note shown on a coming-soon service", "This service is launching soon. Contact us and we'll let you know as soon as it's available.", "Bu xizmat tez orada ishga tushadi. Biz bilan bog'laning — ishga tushishi bilan xabar beramiz.", "Этот сервис скоро запустится. Свяжитесь с нами — мы сообщим, как только он станет доступен."),
    ("services.notify_me", "Service detail page: button on a coming-soon service", "Let me know", "Menga xabar bering", "Сообщите мне"),

    ("services_page.eyebrow", "Services list page eyebrow", "What we offer", "Nimalar taklif qilamiz", "Что мы предлагаем"),
    ("services_page.lead", "Services list page intro", "ELD and dispatch services for trucking companies and owner-operators. Safety and Fleet teams are coming soon.", "Trucking kompaniyalar va truck egalari uchun ELD va dispatch xizmatlari. Safety va Fleet jamoalari tez orada.", "ELD и диспетчерские услуги для траковых компаний и владельцев траков. Отделы Safety и Fleet — скоро."),

    ("whyus.heading_fallback", "Why-choose-us fallback heading", "Your Company's Interests Come First", "Kompaniyangiz manfaatlari birinchi o'rinda", "Интересы вашей компании — на первом месте"),

    ("howitworks.heading", "How it works section heading", "Simple Steps. Reliable Support.", "Oddiy qadamlar. Ishonchli xizmat.", "Простые шаги. Надёжная поддержка."),
    ("howitworks.lead", "How it works section intro", "Tell us about your fleet and we'll take over the logs, the paperwork and the loads.", "Avtoparkingiz haqida ayting — loglar, hujjatlar va yuklarni biz o'z zimmamizga olamiz.", "Расскажите о своём автопарке — логи, документы и грузы мы возьмём на себя."),
    ("howitworks.step1_title", "Step 1 title", "Contact Us", "Biz bilan bog'laning", "Свяжитесь с нами"),
    ("howitworks.step1_desc", "Step 1 description", "Tell us how many trucks you have, which ELD you use and which service you need.", "Nechta truckingiz borligi, qaysi ELD'dan foydalanishingiz va qaysi xizmat kerakligini ayting.", "Расскажите, сколько у вас траков, каким ELD вы пользуетесь и какая услуга нужна."),
    ("howitworks.step2_title", "Step 2 title", "We Connect", "Ulanamiz", "Подключаемся"),
    ("howitworks.step2_desc", "Step 2 description", "We get secure access to your ELD and set up integrations with Highway, Trucking Tools and others.", "ELD tizimingizga xavfsiz ulanamiz va Highway, Trucking Tools kabi tizimlar bilan integratsiyani sozlaymiz.", "Получаем защищённый доступ к вашему ELD и настраиваем интеграции с Highway, Trucking Tools и другими."),
    ("howitworks.step3_title", "Step 3 title", "We Work 24/7", "24/7 ishlaymiz", "Работаем 24/7"),
    ("howitworks.step3_desc", "Step 3 description", "Our team manages logs, audits and loads around the clock while you focus on the road.", "Jamoamiz loglar, auditlar va yuklar bilan kechayu kunduz ishlaydi, siz esa yo'lga e'tibor berasiz.", "Наша команда круглосуточно ведёт логи, аудиты и грузы, а вы сосредоточены на дороге."),

    ("systems.heading", "Systems-we-use section heading (homepage + service page)", "ELD Systems We Work With", "Biz ishlaydigan ELD tizimlari", "ELD-системы, с которыми мы работаем"),
    ("systems.integrated_heading", "Integrated/partner systems heading (service page)", "Systems We Connect With", "Biz bog'lanadigan tizimlar", "Системы, с которыми мы связаны"),

    ("products_page.lead", "Products list page intro", "ELD devices and equipment for your trucks. Send a request and we'll get back to you.", "Yuk mashinalaringiz uchun ELD qurilmalari va uskunalar. So'rov yuboring, sizga javob beramiz.", "ELD-устройства и оборудование для ваших траков. Отправьте запрос, и мы свяжемся с вами."),

    ("news_page.lead", "News list page intro", "Updates about our services, trainings and team.", "Xizmatlarimiz, treninglar va jamoamiz haqidagi yangiliklar.", "Новости о наших услугах, тренингах и команде."),

    ("contact.heading", "Contact page heading", "Let's talk about your trucks", "Truckingiz haqida gaplashaylik", "Давайте обсудим ваши траки"),
    ("contact.lead", "Contact page intro", "Tell us how many trucks you have and which service you need — we'll get back to you shortly. We are available 24/7.", "Nechta truckingiz borligi va qaysi xizmat kerakligini yozing — tez orada javob beramiz. Biz 24/7 aloqadamiz.", "Напишите, сколько у вас траков и какая услуга нужна, — мы скоро ответим. Мы на связи 24/7."),

    ("footer.cta_eyebrow", "Footer CTA eyebrow", "Let's work together", "Birga ishlaylik", "Давайте работать вместе"),
    ("footer.cta_heading", "Footer CTA heading", "Ready to hand over your logs and loads?", "Loglar va yuklarni bizga topshirishga tayyormisiz?", "Готовы доверить нам логи и грузы?"),
    ("footer.tagline", "Small text under the logo in the header", "ELD · Dispatch · Safety · Fleet", "ELD · Dispatch · Safety · Fleet", "ELD · Dispatch · Safety · Fleet"),
]


def seed(apps, schema_editor):
    SiteText = apps.get_model("common", "SiteText")
    for key, description, en, uz, ru in TEXTS:
        SiteText.objects.update_or_create(
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
        ("common", "0004_seed_products_teaser_text"),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
