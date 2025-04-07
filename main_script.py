from llm_query import get_data_for_csv
import csv
import os
import re
import sys

# 🧰 Sicherstellen, dass Sonderzeichen korrekt angezeigt werden
sys.stdout.reconfigure(encoding='utf-8')

# 🧾 Ziel-URL aus Argument
if len(sys.argv) < 2:
    print("❗ Bitte URL angeben")
    sys.exit(1)

target_url = sys.argv[1]
print(f"\n🚀 Starte Verarbeitung für: {target_url}")

# 📁 CSV-Datei
csv_file = "output/impressum_analyse_debug.csv"
csv_header = [
    "Unternehmensname", "Geschäftsführer", "E-Mail-Adresse",
    "Telefonnummer", "Adresse", "HRB-Nummer", "UStID-Nummer", "Website"
]

# 🔍 Funktion zum Parsen der LLM-Ausgabe
def extract_info(text, domain):
    def extract(pattern):
        match = re.search(pattern, text)
        return match.group(1).strip() if match else "N/A"

    return {
        "Unternehmensname": extract(r"Unternehmensname:\s*(.+)"),
        "Geschäftsführer": extract(r"Geschäftsführer:\s*(.+)"),
        "E-Mail-Adresse": extract(r"E-Mail-Adresse:\s*(.+)"),
        "Telefonnummer": extract(r"Telefonnummer:\s*(.+)"),
        "Adresse": extract(r"Adresse:\s*(.+)"),
        "HRB-Nummer": extract(r"HRB-Nummer:\s*(.+)"),
        "UStID-Nummer": extract(r"UStID-Nummer:\s*(.+)"),
        "Website": domain
    }

try:
    # 🧠 LLM aufrufen
    print("🔍 Hole Impressumsdaten vom LLM...")
    text_output = get_data_for_csv(target_url)

    # 📦 Daten extrahieren
    print("🧪 Analysiere LLM-Ausgabe...")
    entry = extract_info(text_output, target_url)

    # 📝 CSV schreiben
    file_exists = os.path.isfile(csv_file)
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=csv_header)
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)

    # ✅ Print-Ausgabe der extrahierten Felder
    print(f"\n✅ Verarbeitung abgeschlossen für: {target_url}\n")
    for key, value in entry.items():
        print(f"{key}: {value}")

except Exception as e:
    print(f"\n❌ Fehler bei {target_url}")
    print("🛠️ Fehlerdetails:", e)