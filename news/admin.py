from django.contrib import admin

from common.admin import CreatedByAdminMixin

from .models import NewsPost


@admin.register(NewsPost)
class NewsPostAdmin(CreatedByAdminMixin, admin.ModelAdmin):
    list_display = ("title_en", "published_at", "is_active")
    list_filter = ("is_active",)
    ordering = ("-published_at",)
