from django.db import models
from django.urls import reverse

from common.models import ContentModel, SubmissionModel


class Product(ContentModel):
    title_en = models.CharField(max_length=150)
    title_uz = models.CharField(max_length=150)
    title_ru = models.CharField(max_length=150)
    description_en = models.TextField()
    description_uz = models.TextField()
    description_ru = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Optional. Leave blank if there's no discount.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title_en"]

    def __str__(self):
        return self.title_en

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.id])

    @property
    def has_discount(self):
        return self.discount_price is not None and self.discount_price < self.price

    @property
    def current_price(self):
        return self.discount_price if self.has_discount else self.price

    @property
    def discount_percent(self):
        if not self.has_discount or not self.price:
            return None
        return round((1 - (self.discount_price / self.price)) * 100)


class ProductImage(ContentModel):
    product = models.ForeignKey(Product, related_name="gallery", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/gallery/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Image for {self.product.title_en}"


class ProductInquiry(SubmissionModel):
    product = models.ForeignKey(Product, related_name="inquiries", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Product inquiries"

    def __str__(self):
        return f"{self.name} — {self.product.title_en}"
