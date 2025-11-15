from django.contrib import admin
from .models import SiteSettings, LiveStream, ShopItem


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "tagline")


@admin.register(LiveStream)
class LiveStreamAdmin(admin.ModelAdmin):
    list_display = ("title", "start_time", "is_live")
    list_filter = ("is_live", "start_time")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(ShopItem)
class ShopItemAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "is_active", "is_sold")
    list_filter = ("is_active", "is_sold")
    prepopulated_fields = {"slug": ("title",)}
