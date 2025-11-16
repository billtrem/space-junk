from django.db import models
from django.utils.text import slugify


# ============================================================
# 1. SITE SETTINGS
# ============================================================
class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, default="Space Junk")
    tagline = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)

    hero_image = models.ImageField(upload_to="hero/", blank=True, null=True)

    contact_email = models.EmailField(blank=True)
    instagram_url = models.URLField(blank=True)
    bandcamp_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    def __str__(self):
        return self.site_name

# ============================================================
# 2. VIDEO FEED
# ============================================================
class VideoFeed(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    # Allow full iframe embed code
    embed_code = models.TextField(
        help_text="Paste FULL iframe embed code (YouTube, Vimeo, Twitch, etc.)"
    )

    is_active = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.is_active:
            VideoFeed.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ============================================================
# 3. LIVE STREAM
# ============================================================
class LiveStream(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    is_live = models.BooleanField(default=False)

    # Allow full iframe embed code
    video_embed_code = models.TextField(
        help_text="Paste FULL iframe embed code for the live stream"
    )

    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-start_time"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.is_live:
            LiveStream.objects.exclude(pk=self.pk).update(is_live=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



# ============================================================
# 4. SHOP ITEMS
# ============================================================
class ShopItem(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="shop/", blank=True, null=True)
    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    purchase_url = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False)

    class Meta:
        ordering = ["title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ============================================================
# 5. EMAIL SUBSCRIBER (REQUIRED FOR CHAT)
# ============================================================
class EmailSubscriber(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-subscribed_at"]

    def __str__(self):
        return self.email


# ============================================================
# 6. CHAT MESSAGE (LINKED TO SUBSCRIBER)
# SAFE: subscriber is now nullable so migration will succeed
# ============================================================
class ChatMessage(models.Model):
    subscriber = models.ForeignKey(
        EmailSubscriber,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages"
    )
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        if self.subscriber:
            return f"{self.subscriber.email}: {self.text[:40]}"
        return f"(Unknown): {self.text[:40]}"


# ============================================================
# 7. SCROLLING TICKER
# ============================================================
class TickerMessage(models.Model):
    message = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.message
