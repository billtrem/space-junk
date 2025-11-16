from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import (
    SiteSettings,
    LiveStream,
    VideoFeed,
    ShopItem,
    ChatMessage,
)


# ============================================================
# HOME PAGE  — livestream + preorder + chaotic chat
# ============================================================
def home(request):
    site = SiteSettings.objects.first()

    # Active livestream (only one should be active)
    live_stream = LiveStream.objects.filter(is_live=True).first()

    # Fallback to a normal video feed
    active_video = None
    if not live_stream:
        active_video = VideoFeed.objects.filter(is_active=True).first()

    # Pick a featured item (first active)
    featured_item = (
        ShopItem.objects.filter(is_active=True)
        .order_by("title")
        .first()
    )

    # Newest → oldest, but reversed in template for natural order
    chat_messages = ChatMessage.objects.order_by("-created_at")[:30]

    context = {
        "site": site,
        "live_stream": live_stream,
        "active_video": active_video,
        "featured_item": featured_item,
        "chat_messages": reversed(chat_messages),  # oldest → newest
    }

    return render(request, "siteapp/home.html", context)


# ============================================================
# TELESHOPPING PAGE — livestream + full chaotic chat
# ============================================================
def teleshopping(request):
    site = SiteSettings.objects.first()

    live_stream = LiveStream.objects.filter(is_live=True).first()

    active_video = None
    if not live_stream:
        active_video = VideoFeed.objects.filter(is_active=True).first()

    chat_messages = ChatMessage.objects.order_by("-created_at")[:60]

    return render(request, "siteapp/tele.html", {
        "site": site,
        "live_stream": live_stream,
        "active_video": active_video,
        "chat_messages": reversed(chat_messages),
    })


# ============================================================
# PRODUCTS PAGE
# ============================================================
def products(request):
    site = SiteSettings.objects.first()
    shop_items = ShopItem.objects.filter(is_active=True).order_by("title")

    return render(
        request,
        "siteapp/products.html",
        {"site": site, "shop_items": shop_items},
    )


# ============================================================
# CONTACT PAGE
# ============================================================
def contact(request):
    site = SiteSettings.objects.first()

    return render(
        request,
        "siteapp/contact.html",
        {"site": site},
    )


# ============================================================
# CHAOTIC CHAT — POST MESSAGE (AJAX)
# Accepts JSON or form POST
# ============================================================
@csrf_exempt
def post_chat_message(request):
    if request.method == "POST":

        # Try JSON first
        try:
            data = json.loads(request.body)
            text = data.get("text", "").strip()
        except Exception:
            # Fallback to form data
            text = request.POST.get("text", "").strip()

        if text:
            ChatMessage.objects.create(text=text)

        return JsonResponse({"status": "ok"})

    return JsonResponse({"error": "Invalid request"}, status=400)


# ============================================================
# CHAOTIC CHAT — GET LATEST MESSAGES (AJAX)
# ============================================================
def get_chat_messages(request):
    messages = ChatMessage.objects.order_by("-created_at")[:50]

    data = [
        {
            "text": m.text,
            "time": m.created_at.strftime("%H:%M:%S"),
        }
        for m in reversed(messages)  # oldest → newest
    ]

    return JsonResponse(data, safe=False)
