"""What the panel manages. Each Resource describes one kind of content: how it
is listed, which fields its form has (grouped in sections) and which child
items are edited on the same page (inlines).

In `sections`, a field written as "title*" is a translated field: the panel
shows title_en / title_uz / title_ru behind the EN / UZ / RU switch."""

from dataclasses import dataclass, field
from functools import lru_cache

from .labels import LANGUAGES


@dataclass
class Inline:
    name: str
    model: type
    title: str
    fields: list
    add_label: str = "Qo'shish"


@dataclass
class Resource:
    slug: str
    model: type
    title: str
    singular: str
    group: str
    icon: str
    columns: list  # (spec, header); spec = "field" or "field|kind"
    sections: list = field(default_factory=list)  # (title, [fields])
    search: list = field(default_factory=list)
    inlines: list = field(default_factory=list)
    readonly: bool = False  # visitor submissions: view and delete only
    readonly_on_edit: list = field(default_factory=list)
    filters: list = field(default_factory=list)  # foreign keys to filter the list by
    can_add: bool = True
    view_on_site: bool = False

    def form_fields(self):
        names = []
        for _title, specs in self.sections:
            names += expand(specs)
        return names


def expand(specs):
    names = []
    for spec in specs:
        if spec.endswith("*"):
            names += [f"{spec[:-1]}_{code}" for code, _ in LANGUAGES]
        else:
            names.append(spec)
    return names


@lru_cache(maxsize=1)
def resources():
    from common.models import SiteText
    from core.models import (
        AboutPage,
        ContactInfo,
        ContactLocation,
        ContactMessage,
        Founder,
        HeroSlide,
        Testimonial,
        WhyChooseUs,
        WhyChooseUsPoint,
        WhyChooseUsStat,
    )
    from news.models import NewsPost
    from portfolio.models import Project
    from prices.models import Price
    from products.models import Product, ProductImage, ProductInquiry
    from services.models import IntegratedSystem, Service, ServiceImage, UsedSystem

    gallery = ["image", "order", "is_active"]
    systems = ["name", "image", "link", "order", "is_active"]

    items = [
        # --- Bosh sahifa -------------------------------------------------
        Resource(
            "hero", HeroSlide, "Hero slaydlar", "Hero slayd", "Bosh sahifa", "image",
            columns=[("image|thumb", ""), ("title_en", "Sarlavha"), ("order", "Tartib"), ("is_active|toggle", "Saytda")],
            sections=[
                ("Matn", ["title*", "description*"]),
                ("Tugma", ["button_name*", "button_url"]),
                ("Rasm yoki video", ["image", "video"]),
                ("Sozlamalar", ["order", "is_active"]),
            ],
            search=["title_en", "title_uz", "title_ru"],
        ),
        Resource(
            "why-us", WhyChooseUs, "\"Nega biz\" bo'limi", "\"Nega biz\" bo'limi", "Bosh sahifa", "star",
            columns=[("heading_en", "Sarlavha"), ("is_active|toggle", "Saytda")],
            sections=[("Sarlavha", ["eyebrow*", "heading*", "intro*"]), ("Sozlamalar", ["is_active"])],
            inlines=[
                Inline("points", WhyChooseUsPoint, "Afzalliklar (kartochkalar)",
                       ["icon", "image", "title*", "short_description*", "order", "is_active"], "Afzallik qo'shish"),
                Inline("stats", WhyChooseUsStat, "Raqamlar (statistika)",
                       ["icon", "number", "label*", "order", "is_active"], "Raqam qo'shish"),
            ],
        ),
        Resource(
            "testimonials", Testimonial, "Mijozlar fikri", "Mijoz fikri", "Bosh sahifa", "chat",
            columns=[("image|thumb", ""), ("name", "Ism"), ("role_en", "Kim"), ("order", "Tartib"), ("is_active|toggle", "Saytda")],
            sections=[("Mijoz", ["name", "role*", "image"]), ("Fikri", ["feedback*"]), ("Sozlamalar", ["order", "is_active"])],
            search=["name", "feedback_en"],
        ),
        # --- Xizmatlar ---------------------------------------------------
        Resource(
            "services", Service, "Xizmatlar", "Xizmat", "Xizmatlar", "briefcase",
            columns=[("title_en", "Nomi"), ("is_coming_soon|bool", "Tez orada"), ("order", "Tartib"), ("is_active|toggle", "Saytda")],
            sections=[
                ("Asosiy", ["title*", "short_name*"]),
                ("Xizmat sahifasi", ["full_info*", "key_points*"]),
                ("Sozlamalar", ["icon", "slug", "order", "is_coming_soon", "is_active"]),
            ],
            search=["title_en", "title_uz", "title_ru"],
            inlines=[
                Inline("gallery", ServiceImage, "Rasmlar galereyasi", gallery, "Rasm qo'shish"),
                Inline("used_systems", UsedSystem, "Biz ishlaydigan tizimlar (ELD va boshqalar)", systems, "Tizim qo'shish"),
                Inline("integrated_systems", IntegratedSystem, "Integratsiya qilingan tizimlar", systems, "Tizim qo'shish"),
            ],
            view_on_site=True,
        ),
        Resource(
            "prices", Price, "Tariflar", "Tarif", "Xizmatlar", "tag",
            columns=[("price_type_label_en", "Tarif"), ("service", "Xizmat"), ("price|money", "Narx"),
                     ("is_featured|bool", "Eng ko'p"), ("order", "Tartib"), ("is_active|toggle", "Saytda")],
            sections=[
                ("Tarif", ["service", "price_type_label*", "price", "period", "note*"]),
                ("Tarifga nimalar kiradi", ["features*"]),
                ("Sozlamalar", ["price_type", "order", "is_featured", "is_active"]),
            ],
            search=["price_type_label_en", "price_type_label_uz"],
            filters=["service"],
        ),
        # --- Mahsulotlar va yangiliklar -----------------------------------
        Resource(
            "products", Product, "Mahsulotlar", "Mahsulot", "Kontent", "box",
            columns=[("title_en", "Nomi"), ("price|money", "Narx"), ("discount_price|money", "Chegirma"),
                     ("order", "Tartib"), ("is_active|toggle", "Saytda")],
            sections=[
                ("Mahsulot", ["title*", "description*"]),
                ("Narx", ["price", "discount_price"]),
                ("Sozlamalar", ["slug", "order", "is_active"]),
            ],
            search=["title_en", "title_uz", "title_ru"],
            inlines=[Inline("gallery", ProductImage, "Rasmlar galereyasi", gallery, "Rasm qo'shish")],
            view_on_site=True,
        ),
        Resource(
            "news", NewsPost, "Yangiliklar", "Yangilik", "Kontent", "news",
            columns=[("image|thumb", ""), ("title_en", "Sarlavha"), ("published_at|date", "Sana"), ("is_active|toggle", "Saytda")],
            sections=[
                ("Yangilik", ["title*", "excerpt*", "body*"]),
                ("Rasm", ["image"]),
                ("Sozlamalar", ["published_at", "slug", "is_active"]),
            ],
            search=["title_en", "title_uz", "title_ru"],
            view_on_site=True,
        ),
        # --- Kompaniya ----------------------------------------------------
        Resource(
            "about", AboutPage, "Biz haqimizda", "\"Biz haqimizda\" sahifasi", "Kompaniya", "info",
            columns=[("title_en", "Sarlavha"), ("is_active|toggle", "Saytda")],
            sections=[
                ("Sarlavha va qisqa matn", ["title*", "short_description*"]),
                ("To'liq matn", ["full_description*"]),
                ("Tugma", ["contact_label*", "contact_url"]),
                ("Rasm va sozlamalar", ["image", "is_active"]),
            ],
        ),
        Resource(
            "founders", Founder, "Asoschilar", "Asoschi", "Kompaniya", "user",
            columns=[("image|thumb", ""), ("name", "Ism"), ("order", "Tartib"), ("is_active|toggle", "Saytda")],
            sections=[("Asoschi", ["name", "description*", "contact", "image"]), ("Sozlamalar", ["order", "is_active"])],
            search=["name"],
        ),
        Resource(
            "contact-info", ContactInfo, "Aloqa ma'lumotlari", "Aloqa ma'lumotlari", "Kompaniya", "phone",
            columns=[("email", "Email"), ("phone", "Telefon"), ("is_active|toggle", "Saytda")],
            sections=[("Aloqa", ["email", "phone", "is_active"])],
            inlines=[Inline("locations", ContactLocation, "Manzillar", ["address*", "map_url", "order", "is_active"], "Manzil qo'shish")],
        ),
        Resource(
            "projects", Project, "Loyihalar (portfolio)", "Loyiha", "Kompaniya", "folder",
            columns=[("image|thumb", ""), ("title_en", "Nomi"), ("client", "Mijoz"), ("order", "Tartib"), ("is_active|toggle", "Saytda")],
            sections=[("Loyiha", ["title*", "summary*", "description*", "client", "image"]), ("Sozlamalar", ["order", "is_active"])],
            search=["title_en", "client"],
        ),
        # --- Murojaatlar --------------------------------------------------
        Resource(
            "messages", ContactMessage, "Aloqa xabarlari", "Xabar", "Murojaatlar", "mail",
            columns=[("name", "Ism"), ("email|email", "Email"), ("message|trunc", "Xabar"), ("created_at|datetime", "Sana")],
            sections=[("Xabar", ["name", "email", "message", "created_at"])],
            search=["name", "email", "message"],
            readonly=True,
            can_add=False,
        ),
        Resource(
            "inquiries", ProductInquiry, "Mahsulot so'rovlari", "So'rov", "Murojaatlar", "inbox",
            columns=[("name", "Ism"), ("email|email", "Email"), ("phone", "Telefon"), ("product", "Mahsulot"), ("created_at|datetime", "Sana")],
            sections=[("So'rov", ["product", "name", "email", "phone", "message", "created_at"])],
            search=["name", "email", "phone", "message"],
            readonly=True,
            can_add=False,
            filters=["product"],
        ),
        # --- Sozlamalar ---------------------------------------------------
        Resource(
            "site-texts", SiteText, "Sayt matnlari", "Sayt matni", "Sozlamalar", "text",
            columns=[("key", "Kalit"), ("value_en|trunc", "Inglizcha"), ("value_uz|trunc", "O'zbekcha"), ("description|trunc", "Qayerda")],
            sections=[("Matn", ["key", "value*"])],
            search=["key", "value_en", "value_uz", "value_ru", "description"],
            readonly_on_edit=["key"],
        ),
    ]
    return {r.slug: r for r in items}


GROUP_ORDER = ["Murojaatlar", "Bosh sahifa", "Xizmatlar", "Kontent", "Kompaniya", "Sozlamalar"]


def navigation():
    groups = {}
    for r in resources().values():
        groups.setdefault(r.group, []).append(r)
    return [(name, groups[name]) for name in GROUP_ORDER if name in groups]
