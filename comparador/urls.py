# Rutas (URLs) de la aplicación "comparador"

from django.urls import path
from . import views

app_name = "comparador"

urlpatterns = [
    # Ruta principal que usa la vista ComparadorView
    path("", views.ComparadorView.as_view(), name="comparar"),
]
