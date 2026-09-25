from django.db import migrations


def seed(apps, schema_editor):
    AboutPage = apps.get_model("core", "AboutPage")
    if AboutPage.objects.exists():
        return
    AboutPage.objects.create(
        eyebrow_en="About us",
        eyebrow_uz="Biz haqimizda",
        eyebrow_ru="О нас",
        heading_en="The team behind Triple Power Team",
        heading_uz="Triple Power Team ortidagi jamoa",
        heading_ru="Команда Triple Power Team",
        lead_en=(
            "We're a logistics team that keeps freight, storage, and customs work "
            "running smoothly so our clients can focus on their own business."
        ),
        lead_uz=(
            "Biz yuk tashish, saqlash va bojxona ishlarini muntazam yuritadigan "
            "logistika jamoasimiz, shunday qilib mijozlarimiz o'z biznesiga e'tibor qaratishlari mumkin."
        ),
        lead_ru=(
            "Мы логистическая команда, которая обеспечивает бесперебойную работу "
            "перевозок, хранения и таможенного оформления, чтобы наши клиенты могли "
            "сосредоточиться на своём бизнесе."
        ),
        story_heading_en="Our story",
        story_heading_uz="Bizning tariximiz",
        story_heading_ru="Наша история",
        story_en=(
            "Triple Power Team started with a simple idea: shippers deserve a "
            "logistics partner that moves fast, communicates clearly, and treats "
            "every shipment like it matters.\n\n(Replace this paragraph with your real story.)"
        ),
        story_uz=(
            "Triple Power Team oddiy g'oyadan boshlandi: yuk egalari tez harakat "
            "qiladigan, aniq muloqot qiladigan va har bir yukni muhim deb biladigan "
            "logistika hamkoriga loyiqdir.\n\n(Bu paragrafni haqiqiy tarixingiz bilan almashtiring.)"
        ),
        story_ru=(
            "Triple Power Team начиналась с простой идеи: грузоотправители "
            "заслуживают логистического партнёра, который работает быстро, чётко "
            "общается и относится к каждой поставке серьёзно.\n\n(Замените этот "
            "абзац на вашу реальную историю.)"
        ),
        mission_heading_en="Our mission",
        mission_heading_uz="Bizning maqsadimiz",
        mission_heading_ru="Наша миссия",
        mission_en=(
            "To give every client the power of a full logistics team — trucking, "
            "warehousing, and customs — without having to manage separate vendors for each."
        ),
        mission_uz=(
            "Har bir mijozga to'liq logistika jamoasi kuchini berish — yuk tashish, "
            "omborxona va bojxona — har biri uchun alohida yetkazib beruvchilar bilan "
            "shug'ullanmasdan."
        ),
        mission_ru=(
            "Дать каждому клиенту возможности полноценной логистической команды — "
            "перевозки, складирование и таможню — без необходимости управлять "
            "отдельными поставщиками для каждого направления."
        ),
    )


def unseed(apps, schema_editor):
    AboutPage = apps.get_model("core", "AboutPage")
    AboutPage.objects.filter(heading_en="The team behind Triple Power Team").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_aboutpage"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
