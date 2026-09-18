from django.db import models


class Service(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    summary = models.CharField(max_length=200)
    description = models.TextField()
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
