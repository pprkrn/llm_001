# webscrape_imprint.py

import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
import csv
import sys
sys.stdout.reconfigure(encoding='utf-8')
# Token-Schätzung: 1 Token ≈ 3.5 Zeichen (grob für Deutsch)
def estimate_tokens(text):
    return int(len(text) / 3.5)

# 🧰 UTF-8 Ausgabe aktivieren
sys.stdout.reconfigure(encoding='utf-8')

def load_impressum_paths(csv_file):
    paths = []
    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    paths.append(row[0].strip())
    except FileNotFoundError:
        print(f"❌ Impressum-Pfade-Datei nicht gefunden: {csv_file}")
    return paths

def extract_domain_name(target_url):
    parsed_url = urlparse(target_url)
    hostname = parsed_url.hostname or ''
    domain_parts = hostname.replace('www.', '').split('.')
    return domain_parts[0] if domain_parts else ''

def generate_impressum_urls(target_url, impressum_paths):
    domain = extract_domain_name(target_url)
    return [path.replace("{domain}", domain) for path in impressum_paths]

def run_scraper(target_url):
    impressum_paths = load_impressum_paths("input/impressum_paths.csv")
    impressum_urls = generate_impressum_urls(target_url, impressum_paths)

    print(f"\n🔎 Starte Impressumssuche auf {target_url} – {time.strftime('%H:%M:%S')}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    for path in impressum_urls:
        url = target_url.rstrip('/') + path
        print(f"🔸 Teste: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"🔹 Status: {response.status_code}")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                # Entferne leere oder irrelevante Tags
                for tag in soup.find_all():
                    if not tag.get_text(strip=True):
                        tag.decompose()

                text = soup.get_text(separator=" ", strip=True)
                token_estimate = estimate_tokens(text)
                print(f"🧮 Geschätzte Tokenanzahl: {token_estimate} Tokens")

                if token_estimate > 8192:
                    print("⚠️ Text ist sehr lang – mögliche Kürzung empfohlen!")

                print(f"\n✅ Impressum gefunden unter: {url}")
                return text, url
        except requests.RequestException as e:
            print(f"⚠️ Fehler bei {url}: {e}")
            continue

    print("❌ Kein Impressum gefunden.")
    return None, target_url