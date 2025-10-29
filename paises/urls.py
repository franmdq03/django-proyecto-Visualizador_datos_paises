# urls.py — Rutas de la aplicación principal (paises)

from django.urls import path
from .views import (
    HomeView,
    CountryListView,
    CountryDetailView,
    SignUpView,
    CustomLoginView,
    CustomLogoutView,
)

urlpatterns = [
    # Página de inicio
    path("", HomeView.as_view(), name="home"),
    # Lista de todos los países
    path("paises/", CountryListView.as_view(), name="country-list"),
    # Detalle de un país específico usando su código CCA3
    path("pais/<str:cca3>/", CountryDetailView.as_view(), name="country-detail"),
    # Registro de usuario
    path("registro/", SignUpView.as_view(), name="signup"),
    # Inicio de sesión
    path("login/", CustomLoginView.as_view(), name="login"),
    # Cierre de sesión
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
