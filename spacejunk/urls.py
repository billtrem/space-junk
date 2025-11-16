from django.contrib import admin
from django.urls import path
from siteapp import views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.home, name="home"),

    # NEW — you forgot these
    path("teleshopping/", views.teleshopping, name="teleshopping"),
    path("products/", views.products, name="products"),
    path("contact/", views.contact, name="contact"),
]
