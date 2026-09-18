from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "summary", "order")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order", "title")
