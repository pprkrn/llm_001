import subprocess
import csv

# 📥 CSV-Datei mit Ziel-URLs
csv_file = "input/urls.csv"
target_urls = []

# 🔄 URLs aus CSV laden
with open(csv_file, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        url = row.get("Target URL")
        if url:
            target_urls.append(url.strip())

# 🔁 Jede Domain einzeln verarbeiten
for url in target_urls:
    print(f"\n🚀 Starte Verarbeitung für: {url}")

    try:
        result = subprocess.run(
            ['python', 'main_script.py', url],
            check=True,
            capture_output=True,
            text=True
        )
        print(f" Erfolgreich verarbeitet: {url}")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f" Fehler bei {url}")
        print(e.stderr)
        continue