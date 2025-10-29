# Vista principal del comparador de países.
# Obtiene datos desde la API de restcountries.com y los envía al template.

from django.shortcuts import render

import requests
from django.views.generic import TemplateView

# Clase principal de la vista del comparador
# Usa una TemplateView para mostrar datos de países en un HTML
class ComparadorView(TemplateView):
    template_name = "comparador.html"

    def get_api_data(self, url):
        """Función helper para llamar a la API y manejar errores."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json(), None
        except requests.RequestException as e:
            return None, f"Error de API: {e}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cca3_pais1 = self.request.GET.get("pais1", None)
        cca3_pais2 = self.request.GET.get("pais2", None)

        context["error"] = None
        context["pais1_data"] = None
        context["pais2_data"] = None

        all_countries_url = "https://restcountries.com/v3.1/all?fields=name,cca3"
        all_countries, error = self.get_api_data(all_countries_url)

        if error:
            context["error"] = error
        else:
            # Ordenamos alfabéticamente
            context["all_countries"] = sorted(
                all_countries, key=lambda x: x["name"]["common"]
            )

        if cca3_pais1:
            data, error = self.get_api_data(
                f"https://restcountries.com/v3.1/alpha/{cca3_pais1}"
            )
            if error:
                context["error"] = error
            else:
                context["pais1_data"] = data[0]

        if cca3_pais2:
            data, error = self.get_api_data(
                f"https://restcountries.com/v3.1/alpha/{cca3_pais2}"
            )
            if error:
                context["error"] = error
            else:
                context["pais2_data"] = data[0]

        context["selected_pais1"] = cca3_pais1
        context["selected_pais2"] = cca3_pais2

        return context
