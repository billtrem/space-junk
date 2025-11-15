from django.shortcuts import render
from .models import SiteSettings, LiveStream, ShopItem


def home(request):
    site = SiteSettings.objects.first()

    live_stream = (
        LiveStream.objects.filter(is_live=True)
        .order_by("-start_time")
        .first()
    )

    past_streams = LiveStream.objects.filter(is_live=False).order_by("-start_time")

    shop_items = ShopItem.objects.filter(is_active=True).order_by("title")

    context = {
        "site": site,
        "live_stream": live_stream,
        "past_streams": past_streams,
        "shop_items": shop_items,
    }
    return render(request, "siteapp/home.html", context)
