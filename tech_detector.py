import requests
import re
import time
from urllib.parse import urlparse

fingerprints = {
    "WordPress": [
        r"wp-content", r"wp-includes", r"wp-json", r"wordpress",
        r"generator\" content=\"wordpress", r"/wp-", r"X-WP-Total", r"X-WP-Nonce"
    ],
    "Wix": [r"wix.com", r"X-Wix-Request-Id"],
    "Shopify": [r"cdn.shopify.com", r"Shopify"],
    "Joomla": [r"Joomla", r"/media/system/js/", r"/templates/"],
    "Drupal": [r"Drupal.settings", r"/sites/default/files/", r"drupal"],
    "React": [r"react", r"data-reactroot", r"id=\"root\""],
    "Angular": [r"angular", r"ng-app", r"ng-controller"],
    "Vue.js": [r"vue", r"id=\"app\"", r"__VUE_DEVTOOLS_GLOBAL_HOOK__"],
    "Laravel": [r"laravel", r"csrf-token", r"XSRF-TOKEN"],
    "Django": [r"django", r"csrftoken", r"/static/admin/"],
    "ASP.NET": [r"asp.net", r"__VIEWSTATE", r"X-Powered-By: ASP.NET"],
    "PHP": [r"php", r"X-Powered-By: PHP"],
    "Node.js": [r"X-Powered-By: Express", r"node"],
    "Squarespace": [r"squarespace.com", r"squarespace-cdn"],
    "Webflow": [r"webflow", r"data-wf-page", r"webflow.js"],
    "Google Sites": [r"googleusercontent.com", r"sites.google.com"],
    "GoDaddy Website Builder": [r"secureservercdn.net", r"WebsiteBuilder"],
    "Bootstrap": [r"bootstrap.min.css", r"bootstrap.js"]
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/125.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive"
}

def detectar_tecnologias(url):
    try:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        print(f"\n🔍 Analizando: {url}")
        response = requests.get(url, timeout=10, headers=HEADERS)
        print(f"🌐 Dirección final: {response.url}")
        print(f"📡 Estado HTTP: {response.status_code}")

        # Si da error, intentamos otra vez tras breve espera
        if response.status_code >= 400:
            print("⚠️ Reintentando con protocolo http...")
            time.sleep(2)
            url = url.replace("https://", "http://")
            response = requests.get(url, timeout=10, headers=HEADERS)
            print(f"🌐 Dirección final (2do intento): {response.url}")
            print(f"📡 Estado HTTP: {response.status_code}")

            if response.status_code >= 400:
                print("❌ El sitio no está disponible o bloquea solicitudes.")
                return

        html = response.text.lower()
        headers = str(response.headers).lower()

        tecnologias_encontradas = []

        for tech, patterns in fingerprints.items():
            for pattern in patterns:
                if re.search(pattern.lower(), html) or re.search(pattern.lower(), headers):
                    tecnologias_encontradas.append(tech)
                    break

        tecnologias_encontradas = list(set(tecnologias_encontradas))

        if tecnologias_encontradas:
            print("\n✅ Tecnologías detectadas:")
            for t in tecnologias_encontradas:
                print(f"  • {t}")
        else:
            print("\n⚠️ No se detectaron tecnologías conocidas.")

        time.sleep(1.5)  # Pequeña pausa para evitar bloqueo

    except requests.exceptions.RequestException as e:
        print(f"❌ Error al analizar la página: {e}")

def main():
    print("=== Detector de Tecnologías Web (v3 con delay) ===")
    url = input("👉 Ingresa la URL o dominio de la web: ").strip()
    detectar_tecnologias(url)

if __name__ == "__main__":
    main()