import requests
from django.views.generic import TemplateView, FormView, View
from requests.exceptions import HTTPError
from django import forms
from django.urls import reverse_lazy
from django.shortcuts import redirect, render


# Vista de la página de inicio
class HomeView(TemplateView):
    template_name = "home.html"


# Vista para mostrar los detalles de un país específico
# Obtiene información desde la API de restcountries usando el código CCA3
class CountryDetailView(TemplateView):
    template_name = "country_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        code = kwargs.get("cca3")
        api_url = f"https://restcountries.com/v3.1/alpha/{code}"

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            context["country"] = response.json()[0]
            context["error"] = None
        except requests.RequestException as e:
            context["country"] = None
            context["error"] = f"Error al cargar datos del país: {e}"

        return context


# Vista para mostrar la lista de países
# Permite filtrar por nombre o región y obtiene los datos desde la API
class CountryListView(TemplateView):
    template_name = "country_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.request.GET.get("q", "")
        region = self.request.GET.get("region", "")

        if query:
            api_url = f"https://restcountries.com/v3.1/name/{query}"
        elif region:
            api_url = f"https://restcountries.com/v3.1/region/{region}"
        else:
            api_url = "https://restcountries.com/v3.1/all?fields=name,capital,population,flags,cca3"

        # 2. Consumir la API
        try:
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()

            if query and region:
                filtered_data = []
                for country in data:
                    if country.get("region") == region:
                        filtered_data.append(country)

                data = filtered_data

            context["countries"] = sorted(data, key=lambda x: x["name"]["common"])
            context["error"] = None

        except HTTPError as e:
            if e.response.status_code == 404:
                context["countries"] = []
                context["error"] = f"No se encontraron países para tu búsqueda."
            else:
                context["countries"] = []
                context["error"] = f"Error de API: {e}"
        except requests.RequestException as e:
            context["countries"] = []
            context["error"] = f"Error de conexión: {e}"

        context["current_query"] = query
        context["current_region"] = region

        return context


# ========================================
# 🔐 NUEVO SISTEMA DE AUTENTICACIÓN BASADO EN SESIÓN
# (sin usar la base de datos ni el modelo User de Django)
# ========================================

# ----------------------------------------
# 🧾 Formulario de registro simple
# ----------------------------------------
class SimpleRegistrationForm(forms.Form):
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Contraseña", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean_password2(self):
        # Validamos que las contraseñas coincidan
        cd = self.cleaned_data
        if cd.get("password") != cd.get("password2"):
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cd.get("password2")


# 🔑 Formulario de inicio de sesión simple
class SimpleLoginForm(forms.Form):
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Contraseña", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


# 👤 Vista de registro de usuario
# Guarda el usuario y la contraseña en la sesión actual
class SignUpView(FormView):
    template_name = "registration/signup.html"
    form_class = SimpleRegistrationForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):

        self.request.session["session_user_username"] = form.cleaned_data["username"]
        self.request.session["session_user_password"] = form.cleaned_data["password"]
        return super().form_valid(form)


# 🔓 Vista de inicio de sesión personalizada
# Verifica los datos contra lo guardado en sesión
class CustomLoginView(FormView):
    template_name = "registration/login.html"
    form_class = SimpleLoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        session_user = self.request.session.get("session_user_username")
        session_pass = self.request.session.get("session_user_password")

        if session_user == username and session_pass == password:
            self.request.session["is_logged_in"] = True
            self.request.session["username"] = username
            return super().form_valid(form)
        else:
            # Error de login
            form.add_error(
                None,
                "Usuario o contraseña incorrectos. (Debes registrarte primero en esta sesión)",
            )
            return self.form_invalid(form)


# 🚪 Vista de cierre de sesión
# Limpia los datos del usuario en la sesión
class CustomLogoutView(View):
    def post(self, request, *args, **kwargs):

        request.session["is_logged_in"] = False
        request.session["username"] = None

        return redirect("home")
