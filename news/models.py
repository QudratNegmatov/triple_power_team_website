from django.db import models
from django.urls import reverse

from common.models import ContentModel


class NewsPost(ContentModel):
    title_en = models.CharField(max_length=150)
    title_uz = models.CharField(max_length=150)
    title_ru = models.CharField(max_length=150)
    excerpt_en = models.CharField(max_length=250, help_text="Short summary shown on the news list page.")
    excerpt_uz = models.CharField(max_length=250)
    excerpt_ru = models.CharField(max_length=250)
    body_en = models.TextField()
    body_uz = models.TextField()
    body_ru = models.TextField()
    image = models.ImageField(upload_to="news/", blank=True, null=True)
    published_at = models.DateTimeField()

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title_en

    def get_absolute_url(self):
        return reverse("news_detail", args=[self.id])
