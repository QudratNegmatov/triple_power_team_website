from ckeditor.fields import RichTextField
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
    """The company's own info block on the About page (and its homepage preview)."""

    title_en = models.CharField(max_length=200)
    title_uz = models.CharField(max_length=200)
    title_ru = models.CharField(max_length=200)
    short_description_en = models.TextField(help_text="Shown on the homepage preview card.")
    short_description_uz = models.TextField()
    short_description_ru = models.TextField()
    full_description_en = RichTextField(help_text="Full write-up shown on the About page.")
    full_description_uz = RichTextField()
    full_description_ru = RichTextField()
    contact_label_en = models.CharField(max_length=50, blank=True, help_text='e.g. "Contact us"')
    contact_label_uz = models.CharField(max_length=50, blank=True)
    contact_label_ru = models.CharField(max_length=50, blank=True)
    contact_url = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="about/", blank=True, null=True)

    class Meta:
        verbose_name = "About page (company info)"
        verbose_name_plural = "About page (company info)"

    def __str__(self):
        return self.title_en


class Founder(ContentModel):
    """One of the company's founders, shown on the About page in an alternating layout."""

    name = models.CharField(max_length=150, help_text="Full name — not translated.")
    description_en = models.TextField(help_text="What they say about themselves.")
    description_uz = models.TextField()
    description_ru = models.TextField()
    contact = models.CharField(
        max_length=150, blank=True, help_text="Email, phone, or a social/profile link."
    )
    image = models.ImageField(upload_to="founders/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class Testimonial(ContentModel):
    """A client quote shown on the homepage (up to 6, rotating 3 at a time)."""

    name = models.CharField(max_length=150, help_text="Full name — not translated.")
    role_en = models.CharField(max_length=150, help_text='Who they are, e.g. "Fleet Owner, Sunrise Logistics"')
    role_uz = models.CharField(max_length=150)
    role_ru = models.CharField(max_length=150)
    feedback_en = models.TextField()
    feedback_uz = models.TextField()
    feedback_ru = models.TextField()
    image = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class ContactInfo(ContentModel):
    """Sitewide contact details (email/phone are data, not translated content)."""

    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Contact info"
        verbose_name_plural = "Contact info"

    def __str__(self):
        return self.email or self.phone or "Contact info"


class ContactLocation(ContentModel):
    contact_info = models.ForeignKey(ContactInfo, related_name="locations", on_delete=models.CASCADE)
    address_en = models.CharField(max_length=250)
    address_uz = models.CharField(max_length=250)
    address_ru = models.CharField(max_length=250)
    map_url = models.CharField(max_length=300, blank=True, help_text="Optional link to a map.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.address_en


class ContactMessage(SubmissionModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"
