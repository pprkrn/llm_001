# 🕸️ Domain-Impressum Extractor

Dieses Projekt dient der automatisierten Extraktion von Impressumsdaten aus einer Liste von Webseiten. Die Verarbeitung erfolgt in mehreren Schritten, von der URL-Eingabe über Scraping bis zur strukturierten Ausgabe über ein spezialisiertes Language Model.

---

## 📦 Projektübersicht

Das Projekt besteht aus drei Hauptkomponenten:

1. **`run_batch_domains.py`** – Batch-Controller zum Einlesen und Starten der Verarbeitung
2. **`main_script.py`** – Einzelverarbeitung einer URL inkl. Ergebnis-Speicherung
3. **`llm_query.py`** – Kommunikation mit einem LLM zur strukturierten Datenausgabe

---

## 📁 Projektstruktur

```
llm_001/
├── input/
│   └── urls.csv                        # CSV-Datei mit den Ziel-URLs
├── output/
│   └── impressum_analyse.csv          # Ergebnisdatei der Datenextraktion
├── main_script.py                     # Einzelverarbeitung
├── run_batch_domains.py               # Batch-Verarbeitung
├── llm_query.py                       # LLM-Logik für Datenanalyse
└── webscrape_imprint.py               # Web-Scraping Modul
```

---

## 🧰 Voraussetzungen

- Python 3.6 oder höher
- Terminal mit UTF-8-Unterstützung
- Lokale Instanz von [`ollama`](https://ollama.com/) mit Modell `pprkrn/imprintextractor:latest` (auf Mistral-Basis mit LoRA-Finetuning)

---

## 🔄 Ablaufbeschreibung

### 1. 🔁 `run_batch_domains.py`

Startet die Batch-Verarbeitung für mehrere URLs aus `input/urls.csv`.

#### Beispiel:

```bash
python run_batch_domains.py
```

### 2. 🧠 `main_script.py`

Verarbeitet eine einzelne Domain:

- Übergibt URL an `llm_query.get_data_for_csv()`
- Analysiert die LLM-Antwort per RegEx
- Schreibt das Ergebnis in `output/impressum_analyse.csv`

#### Beispiel:

```bash
python main_script.py https://example.com
```

### 3. 🤖 `llm_query.py`

Führt folgende Schritte aus:

- Startet Scraper (`run_scraper()`)
- Generiert Prompt mit Zielstruktur
- Übergibt Prompt an das Modell `imprintextractor:latest`
- Erwartet eine Antwort im exakt folgenden Format:

```
Unternehmensname:
Geschäftsführer:
E-Mail-Adresse:
Telefonnummer:
Adresse:
HRB-Nummer:
UStID-Nummer:
Website:
```

**Hinweis:** Wenn Informationen fehlen, wird `"N/A"` zurückgegeben.

---

## 📥 Eingabeformat

Die Datei `input/urls.csv` muss folgendermaßen aufgebaut sein:

```csv
Target URL
https://example.com
https://another-example.org
```

---

## 🧪 Ausgabeformat

Ergebnisse werden automatisch in die Datei `output/impressum_analyse_debug.csv` geschrieben, z. B.:

```csv
Unternehmensname,Geschäftsführer,E-Mail-Adresse,Telefonnummer,Adresse,HRB-Nummer,UStID-Nummer,Website
Example GmbH,Max Mustermann,info@example.com,+49 123 4567,Musterstraße 1,12345 Musterstadt,HRB 12345,DE123456789,https://example.com
```

---

## ⚠️ Fehlerbehandlung

- Bei fehlender Eingabe-URL → Hinweis in der Konsole
- Bei nicht auffindbarem Impressum → `"Kein Impressum gefunden"`
- Fehlerhafte Antwort → Exception Logging mit URL

---

## 📜 Lizenz

Dieses Projekt ist unter der MIT-Lizenz veröffentlicht – siehe [LICENSE](LICENSE).

