from django.contrib import admin

from common.admin import CreatedByAdminMixin
from prices.models import Price

from .models import Service, ServiceImage


class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1
    fields = ("image", "order", "is_active")


class PriceInline(admin.TabularInline):
    model = Price
    extra = 1
    fields = (
        "price_type",
        "price_type_label_en",
        "price_type_label_uz",
        "price_type_label_ru",
        "price",
        "period",
        "order",
        "is_active",
    )


@admin.register(Service)
class ServiceAdmin(CreatedByAdminMixin, admin.ModelAdmin):
    list_display = ("title_en", "order", "is_active", "created_by", "created_at")
    list_editable = ("order", "is_active")
    ordering = ("order", "title_en")
    inlines = [ServiceImageInline, PriceInline]
