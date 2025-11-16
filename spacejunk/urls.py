from django.urls import path, include

urlpatterns = [
    path("", include("siteapp.urls")),
]
