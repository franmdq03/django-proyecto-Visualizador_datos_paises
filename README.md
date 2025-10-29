# 🌍 Explorador de Países (Proyecto Django)

Proyecto final para la materia "Introducción a la Programación Web con Django".

## Descripción Breve

Este es un mini proyecto web desarrollado con Django y Bootstrap 5. Consume la API pública y gratuita de **REST Countries** (`https://restcountries.com/`) para visualizar información detallada de países del mundo. Permite:

* Ver una lista completa de países con su bandera, capital y población.
* Filtrar países por nombre o por región.
* Ver una página de detalle para cada país con información más completa (nombre oficial, subregión, idiomas, monedas, enlace a Google Maps).
* Comparar dos países lado a lado, mostrando sus datos clave.
* Registro e inicio de sesión de usuarios (funcionalidad básica de autenticación de Django).

El proyecto demuestra el uso de Vistas Basadas en Clases (CBV), herencia de plantillas, consumo de APIs externas con `requests`, y diseño responsive con Bootstrap 5.

**Autor:** Francisco Garcia Sorrenti

---

## Pasos para ejecutar en local

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/franmdq03/django-proyecto-Visualizador_datos_paises.git
    cd django-proyecto-Visualizador_datos_paises 
    ```

2.  **(Opcional pero recomendado) Crear y activar un entorno virtual:**
    ```bash
    python -m venv venv
    ```
    *En Windows:*
    ```bash
    .\venv\Scripts\activate
    ```
    *En macOS/Linux:*
    ```bash
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    El proyecto no requiere claves de API. Solo necesitas instalar las librerías de Python listadas en `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplicar migraciones:**
    Esto preparará la base de datos SQLite (necesaria para el sistema de login de Django).
    ```bash
    python manage.py migrate
    ```

5.  **Ejecutar el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```
<<<<<<< HEAD
=======

6.  Abrir el proyecto en tu navegador web visitando `http://127.0.0.1:8000/`.

---
>>>>>>> a88f1df (Subida para produccion)
