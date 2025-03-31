import requests
from bs4 import BeautifulSoup
import time

# 🔧 Impressums-/Legal-Pfade (gekürzt zum Testen – bei Bedarf erweitern)
impressum_paths = [
    "/impressum", "/impressum.html", "/legal-notice", "/kontakt/impressum", "/de/legal/impressum"
]

# 🌍 Ziel-Domain (ändern bei Bedarf)
domain = "https://www.saturn.de"

print(f"🔎 Starte Impressumssuche auf {domain} – {time.strftime('%H:%M:%S')}\n")

found_page = False

# 👉 User-Agent Header gegen Bot-Blocker
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

for path in impressum_paths:
    url = domain.rstrip('/') + path
    print(f"Teste: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code} bei {url}")
        if response.status_code == 200:
            found_page = True
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text(separator=" ", strip=True)

            print(text)
    
    except requests.RequestException as e:
        print(f"⚠️ Fehler bei {url}: {e}")
        continue