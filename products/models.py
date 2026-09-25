from django.db import models
from django.urls import reverse


class Product(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Optional. Leave blank if there's no discount.",
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.slug])

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


class ProductInquiry(models.Model):
    product = models.ForeignKey(Product, related_name="inquiries", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Product inquiries"

    def __str__(self):
        return f"{self.name} — {self.product.title}"
