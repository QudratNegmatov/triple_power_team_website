from django.db import migrations


def seed(apps, schema_editor):
    AboutPage = apps.get_model("core", "AboutPage")
    Founder = apps.get_model("core", "Founder")
    Testimonial = apps.get_model("core", "Testimonial")
    ContactInfo = apps.get_model("core", "ContactInfo")
    ContactLocation = apps.get_model("core", "ContactLocation")

    if not AboutPage.objects.exists():
        AboutPage.objects.create(
            title_en="The team behind Triple Power Team",
            title_uz="Triple Power Team ortidagi jamoa",
            title_ru="Команда Triple Power Team",
            short_description_en=(
                "We're a logistics team that keeps freight, storage, and customs work "
                "running smoothly so our clients can focus on their own business."
            ),
            short_description_uz=(
                "Biz yuk tashish, saqlash va bojxona ishlarini muntazam yuritadigan "
                "logistika jamoasimiz, shunday qilib mijozlarimiz o'z biznesiga e'tibor "
                "qaratishlari mumkin."
            ),
            short_description_ru=(
                "Мы логистическая команда, которая обеспечивает бесперебойную работу "
                "перевозок, хранения и таможенного оформления, чтобы наши клиенты могли "
                "сосредоточиться на своём бизнесе."
            ),
            full_description_en=(
                "<p>Triple Power Team started with a simple idea: shippers deserve a "
                "logistics partner that moves fast, communicates clearly, and treats "
                "every shipment like it matters.</p>"
                "<p>Today we handle freight, warehousing, customs clearance, and fleet "
                "tracking for clients across multiple industries, backed by a modern "
                "fleet and an experienced dispatch team.</p>"
                "<p>(Replace this with your real company story.)</p>"
            ),
            full_description_uz=(
                "<p>Triple Power Team oddiy g'oyadan boshlandi: yuk egalari tez harakat "
                "qiladigan, aniq muloqot qiladigan va har bir yukni muhim deb biladigan "
                "logistika hamkoriga loyiqdir.</p>"
                "<p>Bugungi kunda biz turli sohalardagi mijozlar uchun yuk tashish, "
                "omborxona, bojxona rasmiylashtiruvi va avtoparkni kuzatish xizmatlarini "
                "ko'rsatamiz.</p>"
                "<p>(Buni haqiqiy kompaniya tarixingiz bilan almashtiring.)</p>"
            ),
            full_description_ru=(
                "<p>Triple Power Team начиналась с простой идеи: грузоотправители "
                "заслуживают логистического партнёра, который работает быстро, чётко "
                "общается и относится к каждой поставке серьёзно.</p>"
                "<p>Сегодня мы занимаемся перевозками, складированием, таможенным "
                "оформлением и отслеживанием автопарка для клиентов из разных отраслей.</p>"
                "<p>(Замените этот текст на реальную историю вашей компании.)</p>"
            ),
            contact_label_en="Contact us",
            contact_label_uz="Biz bilan bog'laning",
            contact_label_ru="Свяжитесь с нами",
            contact_url="/contact/",
        )

    if not Founder.objects.exists():
        Founder.objects.create(
            name="Founder Name",
            description_en=(
                "Founder & CEO. Started Triple Power Team to give shippers a logistics "
                "partner they can actually rely on. (Replace this with the founder's real bio.)"
            ),
            description_uz=(
                "Asoschi va bosh direktor. Yuk egalariga ishonishlari mumkin bo'lgan "
                "logistika hamkorini berish uchun Triple Power Team'ni tashkil etdi. "
                "(Buni asoschining haqiqiy tarjimai holi bilan almashtiring.)"
            ),
            description_ru=(
                "Основатель и генеральный директор. Создал Triple Power Team, чтобы дать "
                "грузоотправителям по-настоящему надёжного логистического партнёра. "
                "(Замените это на реальную биографию основателя.)"
            ),
            contact="founder@triplepowerteam.com",
            order=1,
        )

    if not Testimonial.objects.exists():
        testimonials = [
            {
                "name": "Placeholder Client",
                "role_en": "Fleet Owner, Retail Distribution",
                "role_uz": "Avtopark egasi, Chakana savdo distributsiyasi",
                "role_ru": "Владелец автопарка, Розничная дистрибуция",
                "feedback_en": "Since we started shipping with Triple Power Team, our deliveries are always on time and their dispatch team is easy to reach whenever we need them.",
                "feedback_uz": "Triple Power Team bilan ishlay boshlaganimizdan beri yetkazib berishlarimiz har doim o'z vaqtida, dispetcherlik jamoasi bilan bog'lanish ham oson.",
                "feedback_ru": "С тех пор как мы начали работать с Triple Power Team, наши доставки всегда вовремя, а с их диспетчерской командой легко связаться.",
                "order": 1,
            },
            {
                "name": "Placeholder Client",
                "role_en": "Operations Manager, Import Business",
                "role_uz": "Operatsiyalar menejeri, Import biznesi",
                "role_ru": "Операционный менеджер, Импортный бизнес",
                "feedback_en": "Their customs team handled our import paperwork end to end. What used to take us days now takes hours.",
                "feedback_uz": "Ularning bojxona jamoasi import hujjatlarimiz bilan boshidan oxirigacha shug'ullandi. Avval kunlar ketadigan ish endi soatlab bajariladi.",
                "feedback_ru": "Их таможенная команда полностью оформила наши импортные документы. То, что раньше занимало дни, теперь занимает часы.",
                "order": 2,
            },
            {
                "name": "Placeholder Client",
                "role_en": "Founder, Food Distributor",
                "role_uz": "Asoschi, Oziq-ovqat distributor kompaniyasi",
                "role_ru": "Основатель, Дистрибьютор продуктов питания",
                "feedback_en": "Real-time tracking gives our customers confidence, and the warehousing team keeps our cold chain intact every time.",
                "feedback_uz": "Real vaqtda kuzatuv mijozlarimizga ishonch beradi, omborxona jamoasi esa sovuq zanjirimizni har doim saqlab qoladi.",
                "feedback_ru": "Отслеживание в реальном времени вызывает доверие наших клиентов, а складская команда всегда сохраняет нашу холодовую цепь.",
                "order": 3,
            },
        ]
        for data in testimonials:
            Testimonial.objects.create(**data)

    if not ContactInfo.objects.exists():
        info = ContactInfo.objects.create(
            email="info@triplepowerteam.com",
            phone="+1 (555) 010-0100",
        )
        ContactLocation.objects.create(
            contact_info=info,
            address_en="1200 Logistics Way, Chicago, IL, USA",
            address_uz="1200 Logistics Way, Chikago, Illinoys, AQSH",
            address_ru="1200 Logistics Way, Чикаго, Иллинойс, США",
            order=1,
        )


def unseed(apps, schema_editor):
    AboutPage = apps.get_model("core", "AboutPage")
    Founder = apps.get_model("core", "Founder")
    Testimonial = apps.get_model("core", "Testimonial")
    ContactInfo = apps.get_model("core", "ContactInfo")
    AboutPage.objects.filter(title_en="The team behind Triple Power Team").delete()
    Founder.objects.filter(name="Founder Name").delete()
    Testimonial.objects.filter(name="Placeholder Client").delete()
    ContactInfo.objects.filter(email="info@triplepowerteam.com").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_aboutpage_contactinfo_contactlocation_founder_and_more"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
