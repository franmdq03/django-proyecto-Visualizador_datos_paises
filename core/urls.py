# urls.py — Archivo principal de rutas del proyecto Django

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("paises.urls")),
    path("comparar/", include("comparador.urls")),
]
