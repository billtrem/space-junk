from django.contrib import admin
from .models import (
    SiteSettings,
    LiveStream,
    ShopItem,
    VideoFeed,
    EmailSubscriber,
    ChatMessage,
    TickerMessage,
)

# -----------------------------
# 1. Site Settings
# -----------------------------
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "tagline")


# -----------------------------
# 2. Video Feed
# -----------------------------
@admin.register(VideoFeed)
class VideoFeedAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


# -----------------------------
# 3. Live Streams
# -----------------------------
@admin.register(LiveStream)
class LiveStreamAdmin(admin.ModelAdmin):
    list_display = ("title", "start_time", "is_live")
    list_filter = ("is_live", "start_time")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


# -----------------------------
# 4. Shop Items
# -----------------------------
@admin.register(ShopItem)
class ShopItemAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "is_active", "is_sold")
    list_filter = ("is_active", "is_sold")
    prepopulated_fields = {"slug": ("title",)}


# -----------------------------
# 5. Email Subscribers
# -----------------------------
@admin.register(EmailSubscriber)
class EmailSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "subscribed_at", "is_active")
    search_fields = ("email", "name")
    list_filter = ("is_active",)


# -----------------------------
# 6. Chat Messages
# -----------------------------
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("subscriber", "text", "created_at")
    search_fields = ("text", "subscriber__email")


# -----------------------------
# 7. Scrolling Ticker
# -----------------------------
@admin.register(TickerMessage)
class TickerMessageAdmin(admin.ModelAdmin):
    list_display = ("message", "is_active", "created_at")
    list_filter = ("is_active",)
