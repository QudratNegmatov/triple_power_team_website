from django.contrib import admin

from common.admin import CreatedByAdminMixin

from .models import Price


@admin.register(Price)
class PriceAdmin(CreatedByAdminMixin, admin.ModelAdmin):
    list_display = ("service", "price_type_label_en", "price", "period", "is_active")
    list_filter = ("period", "is_active", "service")
    ordering = ("service", "order")
