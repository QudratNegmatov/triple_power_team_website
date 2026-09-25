from django.db import migrations

# (key, description, value_en, value_uz, value_ru)
TEXTS = [
    ("nav.home", "Nav link: Home", "Home", "Bosh sahifa", "Главная"),
    ("nav.about", "Nav link: About", "About", "Biz haqimizda", "О нас"),
    ("nav.services", "Nav link: Services", "Services", "Xizmatlar", "Услуги"),
    ("nav.products", "Nav link: Products", "Products", "Mahsulotlar", "Товары"),
    ("nav.portfolio", "Nav link: Portfolio", "Portfolio", "Portfolio", "Портфолио"),
    ("nav.news", "Nav link: News", "News", "Yangiliklar", "Новости"),
    ("nav.contact", "Nav link / button: Contact", "Contact", "Aloqa", "Контакты"),

    ("marquee.item1", "Scrolling ticker word 1", "Freight", "Yuk tashish", "Грузоперевозки"),
    ("marquee.item2", "Scrolling ticker word 2", "Warehousing", "Omborxona", "Складирование"),
    ("marquee.item3", "Scrolling ticker word 3", "Customs Clearance", "Bojxona rasmiylashtiruvi", "Таможенное оформление"),
    ("marquee.item4", "Scrolling ticker word 4", "Fleet Tracking", "Avtoparkni kuzatish", "Отслеживание автопарка"),
    ("marquee.item5", "Scrolling ticker word 5", "Cold Chain", "Sovuq zanjir", "Холодовая цепь"),
    ("marquee.item6", "Scrolling ticker word 6", "Import & Export", "Import va eksport", "Импорт и экспорт"),

    ("hero.eyebrow", "Homepage hero eyebrow label", "All-in-one logistics solutions", "Barcha logistika yechimlari bir joyda", "Комплексные логистические решения"),
    ("hero.heading", "Homepage hero headline (line break kept as-is)", "Your Cargo. Our Network.\nDelivered On Time.", "Yukingiz. Bizning tarmog'imiz.\nO'z vaqtida yetkaziladi.", "Ваш груз. Наша сеть.\nДоставка вовремя."),
    ("hero.lead", "Homepage hero paragraph", "Triple Power Team plans and runs the freight, storage, and customs work behind your supply chain — with real-time tracking, so your goods arrive on time, every time.", "Triple Power Team yetkazib berish zanjiringiz ortidagi yuk tashish, saqlash va bojxona ishlarini rejalashtiradi va boshqaradi — real vaqtda kuzatuv bilan, shunday qilib yukingiz har doim o'z vaqtida yetib boradi.", "Triple Power Team планирует и выполняет перевозки, хранение и таможенное оформление в вашей цепочке поставок — с отслеживанием в реальном времени, чтобы груз всегда прибывал вовремя."),
    ("hero.feature1", "Hero checklist item 1", "Real-time tracking", "Real vaqtda kuzatuv", "Отслеживание в реальном времени"),
    ("hero.feature2", "Hero checklist item 2", "24/7 dispatch", "24/7 dispetcherlik", "Диспетчерская служба 24/7"),
    ("hero.feature3", "Hero checklist item 3", "Customs handled", "Bojxona bilan ishlaymiz", "Таможенное оформление"),
    ("hero.feature4", "Hero checklist item 4", "Fleet management", "Avtoparkni boshqarish", "Управление автопарком"),
    ("hero.cta_quote", "Button: Request a quote (used in several places)", "Request a quote", "Narx so'rash", "Запросить цену"),
    ("hero.cta_services", "Button: See our services", "See our services", "Xizmatlarimizni ko'rish", "Посмотреть наши услуги"),

    ("services.eyebrow", "Homepage services section eyebrow", "Our services", "Xizmatlarimiz", "Наши услуги"),
    ("services.heading", "Homepage services section heading", "Complete Logistics Solutions", "To'liq logistika yechimlari", "Комплексные логистические решения"),
    ("services.explore", "Button: Explore all services", "Explore all services", "Barcha xizmatlarni ko'rish", "Смотреть все услуги"),
    ("services.other_heading", "Service detail page: other services heading", "Other services", "Boshqa xizmatlar", "Другие услуги"),
    ("services.back", "Link back to services list", "All services", "Barcha xizmatlar", "Все услуги"),

    ("services_page.eyebrow", "Services list page eyebrow", "What we offer", "Nimalar taklif qilamiz", "Что мы предлагаем"),
    ("services_page.heading", "Services list page heading", "Services", "Xizmatlar", "Услуги"),
    ("services_page.lead", "Services list page intro", "Everything you need to plan, move, store, and clear your cargo.", "Yukingizni rejalashtirish, tashish, saqlash va rasmiylashtirish uchun kerak bo'lgan hamma narsa.", "Всё необходимое для планирования, перевозки, хранения и таможенного оформления вашего груза."),

    ("about.eyebrow", "About page eyebrow", "About us", "Biz haqimizda", "О нас"),
    ("about.nav_title", "About page browser-tab title", "About", "Biz haqimizda", "О нас"),
    ("about.read_more", "Button: Read more (About preview on homepage)", "Read more", "Batafsil", "Подробнее"),
    ("about.founders_heading", "About page: founders section heading", "Our Founders", "Bizning asoschilarimiz", "Наши основатели"),

    ("whyus.eyebrow_fallback", "Why-choose-us fallback eyebrow (shown only if no section is set up yet)", "Why choose us", "Nega bizni tanlashadi", "Почему выбирают нас"),
    ("whyus.heading_fallback", "Why-choose-us fallback heading", "Built for Reliable Delivery. Designed for Your Business.", "Ishonchli yetkazib berish uchun yaratilgan. Biznesingiz uchun mo'ljallangan.", "Создано для надёжной доставки. Разработано для вашего бизнеса."),

    ("howitworks.eyebrow", "How it works section eyebrow", "How it works", "Qanday ishlaydi", "Как это работает"),
    ("howitworks.heading", "How it works section heading", "Simple Steps. Reliable Delivery.", "Oddiy qadamlar. Ishonchli yetkazib berish.", "Простые шаги. Надёжная доставка."),
    ("howitworks.lead", "How it works section intro", "Get a quote in minutes and let us handle the rest, from pickup to final delivery.", "Bir necha daqiqada narx oling, qolganini bizga qoldiring — olib ketishdan yakuniy yetkazib berishgacha.", "Получите расчёт за минуты, а остальное доверьте нам — от забора груза до финальной доставки."),
    ("howitworks.step1_title", "Step 1 title", "Request a Quote", "Narx so'rang", "Запросите цену"),
    ("howitworks.step1_desc", "Step 1 description", "Tell us what you're shipping, where it's going, and when.", "Nimani, qayerga va qachon yuborayotganingizni ayting.", "Расскажите, что, куда и когда вы отправляете."),
    ("howitworks.step2_title", "Step 2 title", "We Plan the Route", "Marshrutni rejalashtiramiz", "Мы планируем маршрут"),
    ("howitworks.step2_desc", "Step 2 description", "We arrange freight, warehousing, and customs clearance.", "Yuk tashish, saqlash va bojxona rasmiylashtiruvini tashkil qilamiz.", "Организуем перевозку, хранение и таможенное оформление."),
    ("howitworks.step3_title", "Step 3 title", "Cargo Delivered", "Yuk yetkazildi", "Груз доставлен"),
    ("howitworks.step3_desc", "Step 3 description", "Track your shipment in real time until it arrives.", "Yukingiz yetib borgunga qadar real vaqtda kuzating.", "Отслеживайте груз в реальном времени до его прибытия."),

    ("portfolio.heading", "Homepage portfolio section heading", "Recent work", "So'nggi ishlar", "Недавние работы"),
    ("portfolio.all", "Button: All projects", "All projects", "Barcha loyihalar", "Все проекты"),
    ("portfolio_page.eyebrow", "Portfolio list page eyebrow", "Our work", "Bizning ishlarimiz", "Наши работы"),
    ("portfolio_page.heading", "Portfolio list page heading", "Portfolio", "Portfolio", "Портфолио"),
    ("portfolio_page.lead", "Portfolio list page intro", "A selection of projects we've delivered for our clients.", "Mijozlarimiz uchun bajargan loyihalarimizdan ba'zilari.", "Подборка проектов, реализованных для наших клиентов."),

    ("systems.heading", "Systems-we-use section heading (homepage + service page)", "Systems We Use", "Biz foydalanadigan tizimlar", "Системы, которые мы используем"),
    ("systems.integrated_heading", "Integrated/partner systems heading (service page)", "Systems We Integrate With", "Biz bog'langan tizimlar", "Системы, с которыми мы интегрированы"),

    ("testimonials.eyebrow", "Testimonials section eyebrow", "What clients say", "Mijozlar fikri", "Отзывы клиентов"),

    ("products_page.eyebrow", "Products list page eyebrow", "Shop", "Do'kon", "Магазин"),
    ("products_page.heading", "Products list page heading", "Products", "Mahsulotlar", "Товары"),
    ("products_page.lead", "Products list page intro", "ELD devices and fleet equipment. Request a quote and we'll get back to you.", "ELD qurilmalari va avtopark uskunalari. So'rov yuboring, sizga javob beramiz.", "ELD-устройства и оборудование для автопарка. Отправьте запрос, и мы свяжемся с вами."),
    ("products.request_heading", "Product detail: inquiry form heading", "Request this product", "Ushbu mahsulotni so'rash", "Запросить этот товар"),
    ("products.submit", "Product inquiry submit button", "Send request", "So'rov yuborish", "Отправить запрос"),
    ("products.other_heading", "Product detail: other products heading", "Other products", "Boshqa mahsulotlar", "Другие товары"),
    ("products.back", "Link back to products list", "All products", "Barcha mahsulotlar", "Все товары"),

    ("news_page.eyebrow", "News list page eyebrow", "Latest updates", "So'nggi yangiliklar", "Последние новости"),
    ("news_page.heading", "News list page heading", "News", "Yangiliklar", "Новости"),
    ("news_page.lead", "News list page intro", "Updates from our fleet, warehouses, and operations.", "Avtopark, omborlar va faoliyatimizdagi yangiliklar.", "Новости о нашем автопарке, складах и операциях."),
    ("news.back", "Link back to news list", "Back to News", "Yangiliklarga qaytish", "Назад к новостям"),

    ("contact.eyebrow", "Contact page eyebrow", "Get in touch", "Bog'laning", "Свяжитесь с нами"),
    ("contact.heading", "Contact page heading", "Let's talk about your project", "Loyihangiz haqida gaplashaylik", "Обсудим ваш проект"),
    ("contact.lead", "Contact page intro", "Tell us a bit about what you need and we'll get back to you shortly.", "Sizga nima kerakligini qisqacha yozing, tez orada javob beramiz.", "Расскажите немного о том, что вам нужно, и мы скоро свяжемся с вами."),
    ("contact.submit", "Contact form submit button", "Send message", "Xabar yuborish", "Отправить сообщение"),
    ("contact.email_label", "Contact page: email field label", "Email", "Email", "Email"),
    ("contact.phone_label", "Contact page: phone field label", "Phone", "Telefon", "Телефон"),
    ("contact.locations_label", "Contact page: locations field label", "Locations", "Manzillar", "Адреса"),

    ("pricing.heading", "Service detail page: pricing section heading", "Pricing", "Narxlar", "Цены"),
    ("common.learn_more", "Generic 'Learn more' link on cards", "Learn more", "Batafsil", "Подробнее"),

    ("footer.cta_eyebrow", "Footer CTA eyebrow", "Let's talk logistics", "Logistika haqida gaplashaylik", "Поговорим о логистике"),
    ("footer.cta_heading", "Footer CTA heading", "Ready to move your next shipment?", "Keyingi yukingizni jo'natishga tayyormisiz?", "Готовы отправить следующий груз?"),
    ("footer.cta_button", "Footer CTA button", "Get in touch", "Bog'lanish", "Связаться"),
    ("footer.rights", "Footer copyright line, after the year and company name", "All rights reserved.", "Barcha huquqlar himoyalangan.", "Все права защищены."),
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


def unseed(apps, schema_editor):
    SiteText = apps.get_model("common", "SiteText")
    SiteText.objects.filter(key__in=[t[0] for t in TEXTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
