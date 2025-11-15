from django.db import models


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


class LiveStream(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    is_live = models.BooleanField(
        default=False,
        help_text="Tick if this is the current live stream",
    )
    video_embed_url = models.URLField(help_text="Embed URL (YouTube, Twitch, etc.)")
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-start_time"]

    def __str__(self):
        return self.title


class ShopItem(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="shop/", blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    purchase_url = models.URLField(
        blank=True,
        help_text="External link to buy / more info",
    )
    is_active = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
