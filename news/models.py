from django.db import models
from django.urls import reverse


class NewsPost(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    excerpt = models.CharField(max_length=250, help_text="Short summary shown on the news list page.")
    body = models.TextField()
    image = models.ImageField(upload_to="news/", blank=True, null=True)
    published_at = models.DateTimeField()
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news_detail", args=[self.slug])
