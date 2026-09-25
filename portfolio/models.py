from django.db import models

from common.models import ContentModel


class Project(ContentModel):
    title_en = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    title_ru = models.CharField(max_length=100)
    summary_en = models.CharField(max_length=200)
    summary_uz = models.CharField(max_length=200)
    summary_ru = models.CharField(max_length=200)
    description_en = models.TextField()
    description_uz = models.TextField()
    description_ru = models.TextField()
    image = models.ImageField(upload_to="portfolio/", blank=True, null=True)
    client = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title_en
