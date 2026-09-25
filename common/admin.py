from django.contrib import admin

from .models import SiteText


class CreatedByAdminMixin:
    """Auto-fills created_by with the logged-in admin user on first save."""

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(SiteText)
class SiteTextAdmin(admin.ModelAdmin):
    list_display = ("key", "description", "value_en")
    search_fields = ("key", "description", "value_en", "value_uz", "value_ru")
    ordering = ("key",)
