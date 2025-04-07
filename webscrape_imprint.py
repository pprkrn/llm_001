# -*- coding: utf-8 -*-
# webscrape_imprint.py
# Web-Scraping-Tool für Impressum-Daten

import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
import csv
import sys
sys.stdout.reconfigure(encoding='utf-8')
    
def load_impressum_paths(csv_file):
    paths = []
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                paths.append(row[0].strip())
    return paths

def extract_domain_name(target_url):
    parsed_url = urlparse(target_url)
    hostname = parsed_url.hostname or ''
    domain_parts = hostname.replace('www.', '').split('.')
    return domain_parts[0] if domain_parts else ''

def generate_impressum_urls(target_url, impressum_paths):
    domain = extract_domain_name(target_url)
    return [path.replace("{domain}", domain) for path in impressum_paths]

def run_scraper(target_url):  # <== WICHTIG: diese Funktion muss da sein
    impressum_paths = load_impressum_paths("input/impressum_paths.csv")
    impressum_urls = generate_impressum_urls(target_url, impressum_paths)

    print(f"Starte Impressumssuche auf {target_url} – {time.strftime('%H:%M:%S')}\n")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    for path in impressum_urls:
        url = target_url.rstrip('/') + path
        print(f"Teste: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {response.status_code} bei {url}")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text(separator=" ", strip=True)
                print(f"\n Impressum gefunden unter: {url}\n")
                print(text)
                return text, target_url
        except requests.RequestException as e:
            print(f" Fehler bei {url}: {e}")
            continue

    print("\n Kein Impressum gefunden.")
    return None, target_url