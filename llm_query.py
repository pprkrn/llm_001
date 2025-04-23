from ollama import chat
from webscrape_imprint import run_scraper
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

def get_data_for_csv(target_url):
    print(f"🚀 Starte Verarbeitung für: {target_url}")

    try:
        print("🔍 Starte Scraper...")
        llm_text_input, html_url = run_scraper(target_url)

        if not llm_text_input:
            print("⚠️ Kein Impressumstext gefunden.")
            return "Kein Impressum gefunden"

        print("✅ Impressumstext gefunden – Länge:", len(llm_text_input), "Zeichen")
        # Optional: Vorschau
        print("📄 Textvorschau:\n", llm_text_input[:500], "...\n")

        extracted_data = """
        Unternehmensname:
        Geschäftsführer:
        E-Mail-Adresse:
        Telefonnummer:
        Adresse:
        HRB-Nummer:
        UStID-Nummer:
        Website:
        """

        prompt_template = (
            "Du bist ein hochqualifizierter Experte für Datenextraktion und Textanalyse. "
            "Deine Aufgabe ist es, aus Impressums-Texten strukturierte, geschäftsrelevante Kontaktdaten zu extrahieren.\n\n"
            "Bitte extrahiere die folgenden Informationen:\n"
            "{extracted_data}\n\n"
            "Der folgende Text wurde von einer Impressumsseite extrahiert:\n\n"
            "{llm_text_input}\n\n"
            "Achte besonders auf Geschäftsführer, Adresse und Kontaktinformationen. "
            "Wenn etwas nicht vorhanden ist, gib 'N/A' zurück.\n\n"
            "Gib die Daten ausschließlich im folgenden Format zurück:\n{extracted_data}\n"
            "Keine Erklärungen oder Kommentare."
        )

        prompt = prompt_template.format(
            llm_text_input=llm_text_input,
            extracted_data=extracted_data
        )

        print("💬 Sende Prompt an LLM...")
        stream = chat(
            model='pprkrn/imprintextractor:latest',
            messages=[{
                'role': 'user',
                'content': prompt,
            }],
            stream=True,
        )

        buffer = ""
        for chunk in stream:
            content = chunk['message']['content']
            buffer += content

        print("✅ Antwort erhalten von LLM")
        clean_output = re.sub(r'<think>.*?</think>', '', buffer, flags=re.DOTALL)

        print("📦 Extraktion abgeschlossen.\n")
        return clean_output.strip()

    except Exception as e:
        print(f"❌ Fehler bei {target_url}")
        print("🛠️ Fehlerdetails:", e)
        return "Fehler bei Verarbeitung"