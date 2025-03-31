import csv
import os
import re
import time
from llm_query import data_for_csv
from webscrape_imprint import domain
#import subprocess


#subprocess.run(['python', 'webscrape_imprint.py'])
#subprocess.run(['python', 'llm_query.py'])


# 📁 CSV-Datei vorbereiten
csv_file = "impressum_analyse_debug.csv"
csv_header = ["Unternehmensname", "Geschäftsführer", "E-Mail-Adresse", "Telefonnummer", "Adresse", "HRB-Nummer", "UStID-Nummer", "Website"]

# 🧾 Input-Variable aus anderem Modul
input_string = data_for_csv

# 🔍 Funktion zum Extrahieren der Infos (Website kommt aus 'domain')
def extract_info(text, domain):
    def extract(pattern):
        match = re.search(pattern, text)
        return match.group(1).strip() if match else "N/A"

    return {
        "Unternehmensname": extract(r"\*\*Unternehmensname:\*\*\s*(.+)"),
        "Geschäftsführer": extract(r"\*\*Geschäftsführer:\*\*\s*(.+)"),
        "E-Mail-Adresse": extract(r"\*\*E-Mail-Adresse:\*\*\s*(.+)"),
        "Telefonnummer": extract(r"\*\*Telefonnummer:\*\*\s*(.+)"),
        "Adresse": extract(r"\*\*Adresse:\*\*\s*(.+)"),
        "HRB-Nummer": extract(r"\*\*HRB-Nummer:\*\*\s*(.+)"),
        "UStID-Nummer": extract(r"\*\*UStID-Nummer:\*\*\s*(.+)"),
        "Website": domain
    }

# 📦 Daten extrahieren
eintrag = extract_info(input_string, domain)

# 📝 Datei öffnen und ggf. Header schreiben
file_exists = os.path.isfile(csv_file)

with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=csv_header)
    if not file_exists:
        writer.writeheader()
    writer.writerow(eintrag)