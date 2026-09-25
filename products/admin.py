from django.contrib import admin

from common.admin import CreatedByAdminMixin

from .models import Product, ProductImage, ProductInquiry


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "order", "is_active")


@admin.register(Product)
class ProductAdmin(CreatedByAdminMixin, admin.ModelAdmin):
    list_display = ("title_en", "price", "discount_price", "is_active", "order")
    list_filter = ("is_active",)
    ordering = ("order", "title_en")
    inlines = [ProductImageInline]


@admin.register(ProductInquiry)
class ProductInquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "product", "created_at")
    list_filter = ("product",)
    readonly_fields = ("product", "name", "email", "phone", "message", "created_at")
