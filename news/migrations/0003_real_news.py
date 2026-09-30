"""Replace the demo logistics news posts with announcements about Triple
Power Team's real services."""

import datetime

from django.db import migrations
from django.utils import timezone

OLD_DEMO_TITLES = [
    "New Warehouse Opens in the North Region",
    "Fleet Expansion: 10 New Trucks Added",
    "Faster Customs Clearance Process",
]

POSTS = [
    {
        "title_en": "Safety and Fleet Teams Are Coming Soon",
        "title_uz": "Safety va Fleet jamoalari tez orada",
        "title_ru": "Скоро: отделы Safety и Fleet",
        "excerpt_en": "We are preparing two new services so trucking companies can handle compliance and equipment in one place.",
        "excerpt_uz": "Trucking kompaniyalar compliance va texnika masalalarini bir joyda hal qilishi uchun ikkita yangi xizmat tayyorlayapmiz.",
        "excerpt_ru": "Мы готовим два новых сервиса, чтобы траковые компании решали вопросы безопасности и техники в одном месте.",
        "body_en": "Besides our ELD and dispatch services, we are preparing two new teams.\n\nThe Safety team will take care of FMCSA and DOT compliance, driver qualification files, CSA score monitoring and audit preparation.\n\nThe Fleet team will plan maintenance, find repair shops and roadside assistance, and track permits, registrations, fuel cards and tolls.\n\nWant to be among the first clients? Contact us and we'll let you know as soon as they launch.",
        "body_uz": "ELD va dispatch xizmatlarimizdan tashqari ikkita yangi jamoa tayyorlayapmiz.\n\nSafety jamoasi FMCSA va DOT talablariga muvofiqlik, haydovchilarning malaka hujjatlari, CSA ballarini kuzatish va auditga tayyorlash bilan shug'ullanadi.\n\nFleet jamoasi texnik xizmatni rejalashtiradi, ustaxona va yo'l yordamini topadi, ruxsatnomalar, registratsiya, yoqilg'i kartalari va toll to'lovlarini kuzatadi.\n\nBirinchi mijozlardan bo'lishni xohlaysizmi? Biz bilan bog'laning — ishga tushishi bilan xabar beramiz.",
        "body_ru": "Помимо ELD и диспетчерских услуг, мы готовим два новых отдела.\n\nОтдел Safety займётся соответствием требованиям FMCSA и DOT, квалификационными файлами водителей, контролем CSA-баллов и подготовкой к аудитам.\n\nОтдел Fleet будет планировать обслуживание, искать мастерские и помощь на дороге, контролировать разрешения, регистрации, топливные карты и платные дороги.\n\nХотите стать одним из первых клиентов? Свяжитесь с нами — сообщим сразу после запуска.",
        "days_ago": 1,
    },
    {
        "title_en": "Weekly ELD and HOS Trainings",
        "title_uz": "ELD va HOS bo'yicha haftalik treninglar",
        "title_ru": "Еженедельные тренинги по ELD и HOS",
        "excerpt_en": "Every week we run trainings for drivers and staff on ELD use and hours-of-service rules.",
        "excerpt_uz": "Har hafta haydovchilar va xodimlar uchun ELD'dan foydalanish va HOS qoidalari bo'yicha treninglar o'tkazamiz.",
        "excerpt_ru": "Каждую неделю мы проводим тренинги для водителей и сотрудников по работе с ELD и правилам HOS.",
        "body_en": "Most log violations come from small mistakes. That's why we run weekly trainings for our clients' drivers and office staff.\n\nWe cover how to use the ELD correctly, hours-of-service rules, what to do during a roadside inspection and how to avoid the most common violations.\n\nTrainings are included for our ELD clients. Contact us to join the next session.",
        "body_uz": "Loglardagi ko'p buzilishlar kichik xatolardan kelib chiqadi. Shuning uchun mijozlarimizning haydovchilari va ofis xodimlari uchun har hafta treninglar o'tkazamiz.\n\nTreninglarda ELD'dan to'g'ri foydalanish, HOS qoidalari, yo'lda inspeksiya paytida nima qilish va eng ko'p uchraydigan buzilishlardan qanday saqlanishni o'rgatamiz.\n\nELD mijozlarimiz uchun treninglar xizmatga kiritilgan. Keyingi treningga qo'shilish uchun biz bilan bog'laning.",
        "body_ru": "Большинство нарушений в логах — результат мелких ошибок. Поэтому каждую неделю мы проводим тренинги для водителей и офисных сотрудников наших клиентов.\n\nРазбираем, как правильно пользоваться ELD, правила HOS, что делать при дорожной инспекции и как избежать самых частых нарушений.\n\nДля клиентов ELD-сервиса тренинги включены. Свяжитесь с нами, чтобы присоединиться к следующему занятию.",
        "days_ago": 7,
    },
    {
        "title_en": "2,000+ Trucks and 500+ Audits Supported",
        "title_uz": "2000+ truck va 500+ auditda yordam",
        "title_ru": "2000+ траков и 500+ аудитов",
        "excerpt_en": "Our ELD team has now serviced more than 2,000 trucks and supported over 500 companies through audits.",
        "excerpt_uz": "ELD jamoamiz 2000 dan ortiq truckka xizmat ko'rsatdi va 500 dan ortiq kompaniyaga auditda yordam berdi.",
        "excerpt_ru": "Наша ELD-команда обслужила более 2000 траков и поддержала более 500 компаний на аудитах.",
        "body_en": "Our ELD service has passed an important milestone: more than 2,000 trucks serviced and more than 500 companies supported through audits.\n\nWe work with PandaELD, UzbPrime ELD, BST ELD, Vitality ELD and other ELD systems, and connect them with Highway, Trucking Tools and similar platforms.\n\nThank you to every company that trusts us with their logs. Your company's interests and the security of your data will always come first for us.",
        "body_uz": "ELD xizmatimiz muhim marraga yetdi: 2000 dan ortiq truckka xizmat ko'rsatildi va 500 dan ortiq kompaniyaga auditda yordam berildi.\n\nBiz PandaELD, UzbPrime ELD, BST ELD, Vitality ELD va boshqa ELD tizimlari bilan ishlaymiz hamda ularni Highway, Trucking Tools va shunga o'xshash platformalar bilan bog'laymiz.\n\nLoglarini bizga ishonib topshirgan har bir kompaniyaga rahmat. Kompaniyangiz manfaatlari va ma'lumotlaringiz xavfsizligi biz uchun doim birinchi o'rinda bo'ladi.",
        "body_ru": "Наш ELD-сервис достиг важного рубежа: обслужено более 2000 траков и более 500 компаний получили поддержку на аудитах.\n\nМы работаем с PandaELD, UzbPrime ELD, BST ELD, Vitality ELD и другими ELD-системами и связываем их с Highway, Trucking Tools и похожими платформами.\n\nСпасибо каждой компании, которая доверяет нам свои логи. Интересы вашей компании и безопасность ваших данных всегда будут для нас на первом месте.",
        "days_ago": 14,
    },
]


def seed(apps, schema_editor):
    NewsPost = apps.get_model("news", "NewsPost")
    NewsPost.objects.filter(title_en__in=OLD_DEMO_TITLES).delete()
    now = timezone.now()
    for data in POSTS:
        data = dict(data)
        days_ago = data.pop("days_ago")
        title_en = data.pop("title_en")
        if NewsPost.objects.filter(title_en=title_en).exists():
            continue
        NewsPost.objects.create(
            title_en=title_en,
            **data,
            published_at=now - datetime.timedelta(days=days_ago),
            is_active=True,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0002_seed_news"),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
