from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tele/", views.teleshopping, name="teleshopping"),
    path("products/", views.products, name="products"),
    path("contact/", views.contact, name="contact"),

    # Chat API
    path("chat/post/", views.post_chat_message, name="post_chat_message"),
    path("chat/get/", views.get_chat_messages, name="get_chat_messages"),
]
