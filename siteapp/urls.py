from django.contrib import admin
from django.urls import path

from siteapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tele/', views.teleshopping, name='teleshopping'),
    path('products/', views.products, name='products'),
    path('contact/', views.contact, name='contact'),

    # Chat
    path('chat/post/', views.post_chat_message, name='post_chat_message'),
    path('chat/get/', views.get_chat_messages, name='get_chat_messages'),

    # Email signup
    path('signup-email/', views.signup_email, name='signup_email'),

    # Admin
    path('admin/', admin.site.urls),
]
