from django.contrib import admin

from common.admin import CreatedByAdminMixin

from .models import Project


@admin.register(Project)
class ProjectAdmin(CreatedByAdminMixin, admin.ModelAdmin):
    list_display = ("title_en", "client", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order", "-created_at")
