from django.shortcuts import render
from .models import SiteSettings, LiveStream, ShopItem


def home(request):
    """
    Homepage – shows livestream (if one is active) + featured item + product grid.
    This page extends the base template which includes:
    - Logo on left
    - Red navbar on right
    - Slogan bar always visible
    """

    # Site-wide settings (logo, slogans, colours)
    site = SiteSettings.objects.first()

    # Current active livestream
    live_stream = (
        LiveStream.objects.filter(is_live=True)
        .order_by("-start_time")
        .first()
    )

    # Featured product (currently just first active item alphabetically)
    # NOTE: 'featured_priority' does NOT exist in your model; ordering removed
    featured_item = (
        ShopItem.objects.filter(is_active=True)
        .order_by("title")
        .first()
    )

    # All active shop items for product grid
    shop_items = ShopItem.objects.filter(is_active=True).order_by("title")

    context = {
        "site": site,
        "live_stream": live_stream,
        "featured_item": featured_item,
        "shop_items": shop_items,
    }

    return render(request, "siteapp/home.html", context)


def teleshopping(request):
    """
    Tele-shopping page – shows livestream + space for previous episodes.
    Always wrapped in base template with slogan + navbar.
    """

    site = SiteSettings.objects.first()

    live_stream = (
        LiveStream.objects.filter(is_live=True)
        .order_by("-start_time")
        .first()
    )

    return render(request, "siteapp/tele.html", {
        "site": site,
        "live_stream": live_stream,
    })


def products(request):
    """
    All products page – shows complete active stock list.
    """

    site = SiteSettings.objects.first()
    shop_items = ShopItem.objects.filter(is_active=True).order_by("title")

    return render(request, "siteapp/products.html", {
        "site": site,
        "shop_items": shop_items,
    })


def contact(request):
    """
    Contact page (will style loud + bargain-shop style later).
    """

    site = SiteSettings.objects.first()

    return render(request, "siteapp/contact.html", {
        "site": site,
    })
