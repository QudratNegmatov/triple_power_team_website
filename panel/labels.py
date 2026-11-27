"""Uzbek labels and hints for the fields the panel shows. A translated field
("title_en", "title_uz", "title_ru") is looked up by its base name ("title")."""

LANGUAGES = [("en", "EN"), ("uz", "UZ"), ("ru", "RU")]

LABELS = {
    "title": "Sarlavha",
    "description": "Tavsif",
    "button_name": "Tugma matni",
    "button_url": "Tugma havolasi",
    "image": "Rasm",
    "video": "Video",
    "order": "Tartib raqami",
    "is_active": "Saytda ko'rinadi",
    "eyebrow": "Ustki kichik yozuv",
    "heading": "Sarlavha",
    "intro": "Kirish matni",
    "icon": "Belgi (ikonka)",
    "short_description": "Qisqa tavsif",
    "number": "Raqam",
    "label": "Yozuv",
    "short_name": "Qisqa tavsif",
    "full_info": "To'liq ma'lumot",
    "key_points": "Asosiy imkoniyatlar",
    "is_coming_soon": "\"Tez orada\" belgisi",
    "slug": "Sahifa manzili (URL)",
    "name": "Nomi",
    "link": "Havola",
    "price": "Narx ($)",
    "discount_price": "Chegirmadagi narx ($)",
    "price_type": "Ichki kod",
    "price_type_label": "Tarif nomi",
    "period": "To'lov davri",
    "note": "Narx ostidagi yozuv",
    "features": "Tarifga nimalar kiradi",
    "is_featured": "\"Eng ko'p tanlanadi\" belgisi",
    "service": "Xizmat",
    "excerpt": "Qisqa mazmun",
    "body": "Matn",
    "published_at": "E'lon qilingan sana",
    "full_description": "To'liq tavsif",
    "contact_label": "Tugma matni",
    "contact_url": "Tugma havolasi",
    "contact": "Aloqa (email, telefon yoki havola)",
    "role": "Kim ekani",
    "feedback": "Fikri",
    "email": "Email",
    "phone": "Telefon",
    "address": "Manzil",
    "map_url": "Xarita havolasi",
    "key": "Kalit",
    "value": "Matn",
    "summary": "Qisqacha",
    "client": "Mijoz",
    "product": "Mahsulot",
    "message": "Xabar",
    "created_at": "Sana",
}

HELP = {
    "description": "Qisqa yozing: uzun matn hero qismini buzadi.",
    "button_url": "Saytdagi sahifa uchun qisqa yozing, masalan /services/ yoki /about/. Til avtomatik qo'shiladi.",
    "image": "JPG, PNG yoki WEBP. Katta ekranlar uchun kamida 1920px kenglikda bo'lgani yaxshi.",
    "video": "MP4, iloji boricha 1080p va 5 MB dan kichik. Rasm yoki video — bittasi yetarli.",
    "order": "Kichik raqam oldinda chiqadi.",
    "is_active": "Belgi olib tashlansa, saytda ko'rinmaydi (o'chirilmaydi).",
    "icon": "Rasm yuklanmasa, shu belgi ko'rsatiladi.",
    "key_points": "Har qatorga bittadan yozing.",
    "features": "Har qatorga bittadan yozing.",
    "slug": "Bo'sh qoldirsangiz, inglizcha sarlavhadan avtomatik yaratiladi. Masalan: eld-service",
    "price_type": "Lotin harflarida qisqa kod, masalan basic, standard, premium. Bitta xizmatda takrorlanmasin.",
    "note": "Masalan: Per month per truck. Bo'sh qolsa, \"Bir truck uchun oyiga\" yoziladi.",
    "is_featured": "Bitta xizmatda faqat bitta tarifga belgilang.",
    "is_coming_soon": "Xizmat sahifasi ko'rinadi, lekin \"Tez orada\" deb belgilanadi.",
    "discount_price": "Chegirma bo'lmasa, bo'sh qoldiring.",
    "excerpt": "Yangiliklar ro'yxatida va Google'da ko'rinadigan qisqa matn.",
    "map_url": "Ixtiyoriy: Google Maps havolasi.",
    "key": "Sayt matnni shu kalit orqali topadi. Masalan: nav.home",
}

ICON_CHOICES = [
    ("", "— tanlanmagan —"),
    ("truck", "Yuk mashinasi"),
    ("clock", "Soat"),
    ("shield", "Qalqon"),
    ("map-pin", "Xarita belgisi"),
    ("users", "Odamlar"),
    ("document", "Hujjat"),
    ("check", "Belgi (✓)"),
    ("star", "Yulduz"),
    ("globe", "Globus"),
    ("package", "Quti"),
    ("warehouse", "Ombor"),
    ("dashboard", "Panel"),
]

PERIOD_CHOICES = [("month", "Oylik"), ("year", "Yillik"), ("one_time", "Bir martalik")]


def base_name(field_name):
    for code, _ in LANGUAGES:
        if field_name.endswith(f"_{code}"):
            return field_name[: -len(code) - 1], code
    return field_name, None


def label_for(field_name):
    base, _ = base_name(field_name)
    return LABELS.get(base, base.replace("_", " ").capitalize())


def help_for(field_name):
    base, _ = base_name(field_name)
    return HELP.get(base, "")
