import datetime

from django.db import migrations
from django.utils import timezone

POSTS = [
    {
        "title_en": "New Warehouse Opens in the North Region",
        "title_uz": "Shimoliy mintaqada yangi ombor ochildi",
        "title_ru": "Открыт новый склад в северном регионе",
        "excerpt_en": "We have opened a new 5,000 sqm warehouse to serve clients in the north region.",
        "excerpt_uz": "Shimoliy mintaqadagi mijozlarga xizmat ko'rsatish uchun 5,000 kv.m yangi ombor ochdik.",
        "excerpt_ru": "Мы открыли новый склад площадью 5000 м² для клиентов в северном регионе.",
        "body_en": "We are excited to announce the opening of our newest warehouse facility, adding 5,000 square meters of secure storage capacity to better serve clients in the north region. The facility includes temperature-controlled zones and 24/7 monitoring.\n\n(Replace this with your real announcement.)",
        "body_uz": "Shimoliy mintaqadagi mijozlarga yaxshiroq xizmat ko'rsatish uchun 5,000 kvadrat metrlik xavfsiz saqlash maydoniga ega yangi omborimiz ochilganini e'lon qilishdan mamnunmiz. Bino harorat nazorati ostidagi zonalar va 24/7 kuzatuvga ega.\n\n(Buni haqiqiy e'loningiz bilan almashtiring.)",
        "body_ru": "Мы рады сообщить об открытии нового склада площадью 5000 квадратных метров для клиентов в северном регионе. Объект оснащён зонами с контролем температуры и круглосуточным наблюдением.\n\n(Замените этот текст на реальное объявление.)",
        "days_ago": 3,
    },
    {
        "title_en": "Fleet Expansion: 10 New Trucks Added",
        "title_uz": "Avtopark kengaytirildi: 10 ta yangi yuk mashinasi qo'shildi",
        "title_ru": "Расширение автопарка: добавлено 10 новых грузовиков",
        "excerpt_en": "Our fleet grows by 10 vehicles to support increasing delivery demand.",
        "excerpt_uz": "Yetkazib berish talabining oshishi tufayli avtoparkimiz 10 ta mashinaga kengaydi.",
        "excerpt_ru": "Наш автопарк увеличился на 10 автомобилей для удовлетворения растущего спроса.",
        "body_en": "To keep up with growing demand, we have added 10 new trucks to our fleet this quarter. This expansion allows us to offer more frequent routes and shorter delivery windows for our clients.\n\n(Replace this with your real announcement.)",
        "body_uz": "O'sib borayotgan talabga javob berish uchun bu chorakda avtoparkimizga 10 ta yangi yuk mashinasini qo'shdik. Bu kengayish mijozlarimizga tezroq yetkazib berish imkonini beradi.\n\n(Buni haqiqiy e'loningiz bilan almashtiring.)",
        "body_ru": "Чтобы соответствовать растущему спросу, в этом квартале мы добавили 10 новых грузовиков в наш автопарк. Это позволяет предлагать клиентам более частые рейсы и короткие сроки доставки.\n\n(Замените этот текст на реальное объявление.)",
        "days_ago": 7,
    },
    {
        "title_en": "Faster Customs Clearance Process",
        "title_uz": "Bojxona rasmiylashtiruvi tezlashtirildi",
        "title_ru": "Ускоренный процесс таможенной очистки",
        "excerpt_en": "We streamlined our customs documentation process to cut clearance times.",
        "excerpt_uz": "Rasmiylashtirish vaqtini qisqartirish uchun bojxona hujjatlari jarayonini soddalashtirdik.",
        "excerpt_ru": "Мы оптимизировали процесс таможенного документооборота для сокращения времени очистки.",
        "body_en": "We have partnered with customs authorities to streamline our documentation process, reducing average clearance times. This means faster turnaround for import and export shipments handled by our team.\n\n(Replace this with your real announcement.)",
        "body_uz": "Hujjatlar jarayonini soddalashtirish uchun bojxona organlari bilan hamkorlik qildik, bu o'rtacha rasmiylashtirish vaqtini qisqartiradi.\n\n(Buni haqiqiy e'loningiz bilan almashtiring.)",
        "body_ru": "Мы наладили сотрудничество с таможенными органами для оптимизации документооборота, что сокращает среднее время очистки.\n\n(Замените этот текст на реальное объявление.)",
        "days_ago": 14,
    },
]


def seed(apps, schema_editor):
    NewsPost = apps.get_model("news", "NewsPost")
    now = timezone.now()
    for data in POSTS:
        data = dict(data)
        days_ago = data.pop("days_ago")
        NewsPost.objects.create(
            **data,
            published_at=now - datetime.timedelta(days=days_ago),
            is_active=True,
        )


def unseed(apps, schema_editor):
    NewsPost = apps.get_model("news", "NewsPost")
    NewsPost.objects.filter(title_en__in=[p["title_en"] for p in POSTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
