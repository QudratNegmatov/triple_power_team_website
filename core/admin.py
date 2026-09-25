from django.contrib import admin

from .models import ContactMessage, WhyChooseUs, WhyChooseUsPoint, WhyChooseUsStat


class WhyChooseUsPointInline(admin.TabularInline):
    model = WhyChooseUsPoint
    extra = 1


class WhyChooseUsStatInline(admin.TabularInline):
    model = WhyChooseUsStat
    extra = 1


@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ("heading",)
    inlines = [WhyChooseUsPointInline, WhyChooseUsStatInline]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    readonly_fields = ("name", "email", "message", "created_at")
