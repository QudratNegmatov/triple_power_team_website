from django.db import models
from django.db.models import Q, UniqueConstraint

from common.i18n import get_translated
from common.models import ContentModel


class Price(ContentModel):
    PERIOD_ONE_TIME = "one_time"
    PERIOD_MONTH = "month"
    PERIOD_YEAR = "year"
    PERIOD_CHOICES = [
        (PERIOD_ONE_TIME, "One-time"),
        (PERIOD_MONTH, "Per month"),
        (PERIOD_YEAR, "Per year"),
    ]

    service = models.ForeignKey(
        "services.Service",
        related_name="prices",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Leave blank for a general/standalone price not tied to one service.",
    )
    price_type = models.SlugField(
        max_length=50,
        help_text='Internal tier code, e.g. "simple", "standard", "pro". '
        "A given service can only have one price per tier.",
    )
    price_type_label_en = models.CharField(max_length=50, help_text='Displayed tier name, e.g. "Simple"')
    price_type_label_uz = models.CharField(max_length=50)
    price_type_label_ru = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default=PERIOD_MONTH)
    features_en = models.TextField(blank=True, help_text="One item per line — what's included.")
    features_uz = models.TextField(blank=True)
    features_ru = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "price"]
        constraints = [
            UniqueConstraint(
                fields=["service", "price_type"],
                condition=Q(service__isnull=False),
                name="unique_service_price_type",
            )
        ]

    def __str__(self):
        service_name = self.service.title_en if self.service else "General"
        return f"{service_name} — {self.price_type_label_en}"

    def features_list(self):
        text = get_translated(self, "features")
        return [line.strip() for line in text.splitlines() if line.strip()]
