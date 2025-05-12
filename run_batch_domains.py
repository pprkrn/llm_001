import subprocess
import csv
import sys

# 🧰 Terminal-Ausgabe auf UTF-8 umstellen (Windows)
sys.stdout.reconfigure(encoding='utf-8')

# 📥 CSV-Datei mit Ziel-URLs
csv_file = "input/urls.csv"
target_urls = []

# 🔄 URLs aus CSV laden
try:
    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row.get("Target URL")
            if url:
                url = url.strip()
                if not url.startswith("http://") and not url.startswith("https://"):
                    url = "https://" + url
                target_urls.append(url)
except FileNotFoundError:
    print(f"❌ Datei nicht gefunden: {csv_file}")
    sys.exit(1)

# 📊 Status
print(f"\n📋 {len(target_urls)} URLs gefunden in {csv_file}\n")

# 🔁 Jede Domain einzeln verarbeiten
for idx, url in enumerate(target_urls, start=1):
    print(f"\n🔄 [{idx}/{len(target_urls)}] Verarbeite: {url}")

    try:
        result = subprocess.run(
            ['python', 'main_script.py', url],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ Erfolgreich verarbeitet: {url}")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler bei: {url}")
        print("🛠️ Fehlerdetails:\n", e.stderr.strip())
        continue