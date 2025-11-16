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
    TickerMessage,
    EmailSubscriber,
)


# ============================================================
# HELPER — Retrieve the active ticker
# ============================================================
def get_active_ticker():
    return (
        TickerMessage.objects.filter(is_active=True)
        .order_by("-created_at")
        .first()
    )


# ============================================================
# HOME PAGE
# ============================================================
def home(request):
    site = SiteSettings.objects.first()
    ticker = get_active_ticker()

    live_stream = LiveStream.objects.filter(is_live=True).first()
    active_video = None if live_stream else VideoFeed.objects.filter(is_active=True).first()

    featured_item = (
        ShopItem.objects.filter(is_active=True)
        .order_by("title")
        .first()
    )

    chat_messages = ChatMessage.objects.order_by("-created_at")[:30]

    # 🔥 FIX — YOU WERE MISSING THIS
    shop_items = ShopItem.objects.filter(is_active=True).order_by("title")

    return render(request, "siteapp/home.html", {
        "site": site,
        "ticker": ticker,
        "live_stream": live_stream,
        "active_video": active_video,
        "featured_item": featured_item,
        "chat_messages": reversed(chat_messages),
        "shop_items": shop_items,  # ✅ NOW ADDED
    })


# ============================================================
# TELESHOPPING PAGE
# ============================================================
def teleshopping(request):
    site = SiteSettings.objects.first()
    ticker = get_active_ticker()

    live_stream = LiveStream.objects.filter(is_live=True).first()
    active_video = None if live_stream else VideoFeed.objects.filter(is_active=True).first()

    chat_messages = ChatMessage.objects.order_by("-created_at")[:60]

    return render(request, "siteapp/tele.html", {
        "site": site,
        "ticker": ticker,
        "live_stream": live_stream,
        "active_video": active_video,
        "chat_messages": reversed(chat_messages),
    })


# ============================================================
# PRODUCTS PAGE
# ============================================================
def products(request):
    site = SiteSettings.objects.first()
    ticker = get_active_ticker()
    shop_items = ShopItem.objects.filter(is_active=True).order_by("title")

    return render(request, "siteapp/products.html", {
        "site": site,
        "ticker": ticker,
        "shop_items": shop_items,
    })


# ============================================================
# CONTACT PAGE
# ============================================================
def contact(request):
    site = SiteSettings.objects.first()
    ticker = get_active_ticker()

    return render(request, "siteapp/contact.html", {
        "site": site,
        "ticker": ticker,
    })


# ============================================================
# EMAIL SIGNUP — AJAX
# ============================================================
@csrf_exempt
def signup_email(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    email = data.get("email", "").strip()
    name = data.get("name", "").strip()

    if not email:
        return JsonResponse({"error": "Email required"}, status=400)

    EmailSubscriber.objects.get_or_create(
        email=email,
        defaults={"name": name}
    )

    return JsonResponse({"status": "ok"})


# ============================================================
# CHAT — POST (Requires subscriber)
# ============================================================
@csrf_exempt
def post_chat_message(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    text = data.get("text", "").strip()
    email = data.get("email", "").strip()
    name = data.get("name", "").strip()

    if not text:
        return JsonResponse({"error": "Empty message"}, status=400)

    if not email:
        return JsonResponse({"error": "Email required"}, status=400)

    subscriber, created = EmailSubscriber.objects.get_or_create(
        email=email,
        defaults={"name": name}
    )

    ChatMessage.objects.create(
        subscriber=subscriber,
        text=text
    )

    return JsonResponse({"status": "ok"})


# ============================================================
# CHAT — GET LATEST MESSAGES (SAFE)
# ============================================================
def get_chat_messages(request):
    messages = ChatMessage.objects.order_by("-created_at")[:50]

    data = []
    for m in reversed(messages):
        if m.subscriber:
            name = m.subscriber.name or "Guest"
            email = m.subscriber.email
        else:
            name = "Guest"
            email = ""

        data.append({
            "name": name,
            "email": email,
            "text": m.text,
            "time": m.created_at.strftime("%H:%M:%S"),
        })

    return JsonResponse(data, safe=False)
