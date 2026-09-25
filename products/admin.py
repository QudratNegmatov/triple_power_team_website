from django.contrib import admin

from .models import Product, ProductInquiry


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "discount_price", "is_active", "order")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order", "title")


@admin.register(ProductInquiry)
class ProductInquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "product", "created_at")
    list_filter = ("product",)
    readonly_fields = ("product", "name", "email", "phone", "message", "created_at")
