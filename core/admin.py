from django.contrib import admin

from common.admin import CreatedByAdminMixin

from .models import AboutPage, ContactMessage, HeroSlide, WhyChooseUs, WhyChooseUsPoint, WhyChooseUsStat


class WhyChooseUsPointInline(admin.TabularInline):
    model = WhyChooseUsPoint
    extra = 1
    fields = ("icon", "image", "title_en", "title_uz", "title_ru", "short_description_en", "short_description_uz", "short_description_ru", "order", "is_active")


class WhyChooseUsStatInline(admin.TabularInline):
    model = WhyChooseUsStat
    extra = 1
    fields = ("icon", "number", "label_en", "label_uz", "label_ru", "order", "is_active")


@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(CreatedByAdminMixin, admin.ModelAdmin):
    list_display = ("heading_en", "is_active")
    inlines = [WhyChooseUsPointInline, WhyChooseUsStatInline]


@admin.register(HeroSlide)
class HeroSlideAdmin(CreatedByAdminMixin, admin.ModelAdmin):
    list_display = ("title_en", "order", "is_active", "created_by", "created_at")
    list_editable = ("order", "is_active")
    ordering = ("order",)


@admin.register(AboutPage)
class AboutPageAdmin(CreatedByAdminMixin, admin.ModelAdmin):
    list_display = ("heading_en", "is_active")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    readonly_fields = ("name", "email", "message", "created_at")
