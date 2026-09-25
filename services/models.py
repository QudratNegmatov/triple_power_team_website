from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse

from common.i18n import get_translated
from common.models import ContentModel


class Service(ContentModel):
    title_en = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    title_ru = models.CharField(max_length=100)
    short_name_en = models.CharField(max_length=200, help_text="Short summary shown on cards.")
    short_name_uz = models.CharField(max_length=200)
    short_name_ru = models.CharField(max_length=200)
    full_info_en = RichTextField(help_text="Full description shown on the service's detail page.")
    full_info_uz = RichTextField()
    full_info_ru = RichTextField()
    key_points_en = models.TextField(blank=True, help_text="One item per line.")
    key_points_uz = models.TextField(blank=True)
    key_points_ru = models.TextField(blank=True)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Icon keyword shown next to the title.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title_en"]

    def __str__(self):
        return self.title_en

    def get_absolute_url(self):
        return reverse("service_detail", args=[self.id])

    def key_points_list(self):
        text = get_translated(self, "key_points")
        return [line.strip() for line in text.splitlines() if line.strip()]


class ServiceImage(ContentModel):
    service = models.ForeignKey(Service, related_name="gallery", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="services/gallery/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Image for {self.service.title_en}"
