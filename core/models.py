from django.db import models


class WhyChooseUs(models.Model):
    eyebrow = models.CharField(max_length=100, default="Why choose us")
    heading = models.CharField(max_length=200)
    intro = models.TextField()

    class Meta:
        verbose_name = "Why Choose Us section"
        verbose_name_plural = "Why Choose Us section"

    def __str__(self):
        return self.heading


class WhyChooseUsPoint(models.Model):
    section = models.ForeignKey(WhyChooseUs, related_name="points", on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.text


class WhyChooseUsStat(models.Model):
    section = models.ForeignKey(WhyChooseUs, related_name="stats", on_delete=models.CASCADE)
    icon = models.CharField(
        max_length=50,
        help_text="truck, clock, warehouse, star, shield, users, document, package, map-pin, dashboard, check, globe",
    )
    number = models.CharField(max_length=20, help_text='e.g. "120+" or "99%"')
    label = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.number} {self.label}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"
