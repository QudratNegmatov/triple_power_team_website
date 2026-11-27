from django.contrib import admin

from common.admin import CreatedByAdminMixin

from .models import Price


@admin.register(Price)
class PriceAdmin(CreatedByAdminMixin, admin.ModelAdmin):
    list_display = ("service", "price_type_label_en", "price", "period", "is_active")
    list_filter = ("period", "is_active", "service")
    ordering = ("service", "order")
    fieldsets = (
        (None, {"fields": ("service", "price_type", "price", "period", "order", "is_active")}),
        ("Plan name", {"fields": ("price_type_label_en", "price_type_label_uz", "price_type_label_ru")}),
        ("Line under the price", {"fields": ("note_en", "note_uz", "note_ru")}),
        ("What's included (one item per line)", {"fields": ("features_en", "features_uz", "features_ru")}),
    )
