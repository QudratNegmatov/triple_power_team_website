from django.db import models
from django.urls import reverse


class Service(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    summary = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="services/", blank=True, null=True)
    key_points = models.TextField(
        blank=True,
        help_text="One item per line. Shown as a bullet list on the service's detail page.",
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Optional icon name/emoji shown next to the title.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("service_detail", args=[self.slug])

    def key_points_list(self):
        return [line.strip() for line in self.key_points.splitlines() if line.strip()]
