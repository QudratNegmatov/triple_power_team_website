from django.db import models

from common.models import ContentModel, SubmissionModel


class WhyChooseUs(ContentModel):
    eyebrow_en = models.CharField(max_length=100, default="Why choose us")
    eyebrow_uz = models.CharField(max_length=100, default="Nega bizni tanlashadi")
    eyebrow_ru = models.CharField(max_length=100, default="Почему выбирают нас")
    heading_en = models.CharField(max_length=200)
    heading_uz = models.CharField(max_length=200)
    heading_ru = models.CharField(max_length=200)
    intro_en = models.TextField()
    intro_uz = models.TextField()
    intro_ru = models.TextField()

    class Meta:
        verbose_name = "Why Choose Us section"
        verbose_name_plural = "Why Choose Us section"

    def __str__(self):
        return self.heading_en


class WhyChooseUsPoint(ContentModel):
    section = models.ForeignKey(WhyChooseUs, related_name="points", on_delete=models.CASCADE)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Icon keyword (truck, clock, warehouse, star, shield, users, document, package, map-pin, dashboard, check, globe)",
    )
    image = models.ImageField(upload_to="why_us/", blank=True, null=True)
    title_en = models.CharField(max_length=150)
    title_uz = models.CharField(max_length=150)
    title_ru = models.CharField(max_length=150)
    short_description_en = models.CharField(max_length=250)
    short_description_uz = models.CharField(max_length=250)
    short_description_ru = models.CharField(max_length=250)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title_en


class WhyChooseUsStat(ContentModel):
    section = models.ForeignKey(WhyChooseUs, related_name="stats", on_delete=models.CASCADE)
    icon = models.CharField(
        max_length=50,
        help_text="truck, clock, warehouse, star, shield, users, document, package, map-pin, dashboard, check, globe",
    )
    number = models.CharField(max_length=20, help_text='e.g. "120+" or "99%"')
    label_en = models.CharField(max_length=50)
    label_uz = models.CharField(max_length=50)
    label_ru = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.number} {self.label_en}"


class HeroSlide(ContentModel):
    title_en = models.CharField(max_length=150)
    title_uz = models.CharField(max_length=150)
    title_ru = models.CharField(max_length=150)
    description_en = models.TextField()
    description_uz = models.TextField()
    description_ru = models.TextField()
    button_name_en = models.CharField(max_length=50, blank=True)
    button_name_uz = models.CharField(max_length=50, blank=True)
    button_name_ru = models.CharField(max_length=50, blank=True)
    button_url = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="hero/", blank=True, null=True)
    video = models.FileField(upload_to="hero/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title_en

    def clean(self):
        from django.core.exceptions import ValidationError

        if not self.image and not self.video:
            raise ValidationError("Add either an image or a video for this slide.")


class AboutPage(ContentModel):
    eyebrow_en = models.CharField(max_length=100, default="About us")
    eyebrow_uz = models.CharField(max_length=100, default="Biz haqimizda")
    eyebrow_ru = models.CharField(max_length=100, default="О нас")
    heading_en = models.CharField(max_length=200)
    heading_uz = models.CharField(max_length=200)
    heading_ru = models.CharField(max_length=200)
    lead_en = models.TextField()
    lead_uz = models.TextField()
    lead_ru = models.TextField()
    story_heading_en = models.CharField(max_length=100, default="Our story")
    story_heading_uz = models.CharField(max_length=100, default="Bizning tariximiz")
    story_heading_ru = models.CharField(max_length=100, default="Наша история")
    story_en = models.TextField()
    story_uz = models.TextField()
    story_ru = models.TextField()
    mission_heading_en = models.CharField(max_length=100, default="Our mission")
    mission_heading_uz = models.CharField(max_length=100, default="Bizning maqsadimiz")
    mission_heading_ru = models.CharField(max_length=100, default="Наша миссия")
    mission_en = models.TextField()
    mission_uz = models.TextField()
    mission_ru = models.TextField()
    image = models.ImageField(upload_to="about/", blank=True, null=True)

    class Meta:
        verbose_name = "About page"
        verbose_name_plural = "About page"

    def __str__(self):
        return self.heading_en


class ContactMessage(SubmissionModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"
