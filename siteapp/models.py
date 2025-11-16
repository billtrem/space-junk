from django.db import models
from django.utils.text import slugify


# ============================================================
# 1. SITE SETTINGS
# Global info for the website header, footer, links, etc.
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
# 2. VIDEO FEED (SEPARATE FROM LIVESTREAM)
# Useful for static video embeds, archive episodes,
# or switching from livestream → tape → adverts, etc.
# ============================================================
class VideoFeed(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    embed_url = models.URLField(help_text="Embed URL (YouTube, Vimeo, Twitch, etc.)")
    is_active = models.BooleanField(
        default=False,
        help_text="Tick to make this the default active feed."
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.is_active:
            # deactivate all others
            VideoFeed.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ============================================================
# 3. LIVE STREAM MODEL
# More detailed than VideoFeed; for timed live events.
# ============================================================
class LiveStream(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)

    is_live = models.BooleanField(default=False)
    video_embed_url = models.URLField(help_text="Embed URL to YouTube/Twitch/etc.")
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-start_time"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.is_live:
            # Ensure only one livestream is marked live
            LiveStream.objects.exclude(pk=self.pk).update(is_live=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ============================================================
# 4. SHOP ITEMS
# For physical or digital products
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
# 5. CHAOTIC LIVE CHAT
# Messages appear instantly, no usernames, anon chaos.
# ============================================================
class ChatMessage(models.Model):
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.text[:50]
