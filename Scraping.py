import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse

def download_page(url, folder_name):
    """Descarga y guarda el HTML de una página."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica si hubo un error al descargar

        # Nombre del archivo basado en el path del enlace
        parsed_url = urlparse(url)
        filename = os.path.join(folder_name, f"{parsed_url.path.strip('/').replace('/', '_') or 'index'}.html")

        # Guardar el contenido HTML
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"Página guardada: {filename}")

    except Exception as e:
        print(f"Error al descargar {url}: {e}")

def scrape_and_download_links(base_url, folder_name="pokedex"):
    """Scrapea los enlaces de la página base y los descarga."""
    # Crear la carpeta si no existe
    os.makedirs(folder_name, exist_ok=True)

    # Descargar la página base
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Verifica si hubo un error

        soup = BeautifulSoup(response.text, "html.parser")

        # Extraer y descargar todos los enlaces encontrados
        for link in soup.find_all("a", href=True):
            # Convertir enlaces relativos en absolutos
            full_url = urljoin(base_url, link["href"])

            # Filtrar enlaces para evitar dominios externos
            if urlparse(full_url).netloc == urlparse(base_url).netloc:
                download_page(full_url, folder_name)

    except Exception as e:
        print(f"Error al procesar {base_url}: {e}")

# URL objetivo
base_url = "https://www.wikidex.net/wiki/Lista_de_Pokémon_según_la_Pokédex_de_Kanto"

# Ejecutar la función de scraping y descarga
scrape_and_download_links(base_url)
