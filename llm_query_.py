from ollama import chat
from webscrape_imprint import run_scraper
import re

def get_data_for_csv(target_url):
    llm_text_input, _ = run_scraper(target_url)

    if not llm_text_input:
        return "Kein Impressum gefunden"

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

    # Prompt-Template vorbereiten
    prompt_template = (
        
        #V1
        #"Du bist ein Experte in der Datenextraktion und Textanalyse. "
        #"Deine Aufgabe ist es, einen Text zu analysieren, der von einer Website extrahiert wurde. "
        #"Extrahiere die folgenden Kontaktdaten:\n\n" + llm_text_input +
        #"\n\nGib die Informationen im folgenden Format zurück:\n" + extracted_data +
        #"\nWenn eine Information nicht direkt angegeben ist, aber aus dem Kontext erschlossen werden kann, gib den wahrscheinlichsten Wert an. "
        #"Nur wenn absolut keine Information vorhanden oder ableitbar ist, gib \"N/A\" zurück. "
        #"Gib ausschließlich die extrahierten Daten im genannten Format zurück, ohne zusätzliche Erklärungen oder Kommentare."
        
        #V2
        #"Du bist ein hochqualifizierter Experte für Datenextraktion und Textanalyse. "
        #"Deine Hauptaufgabe besteht darin, aus rechtlich relevanten Texten – insbesondere Impressumsseiten – strukturierte Kontaktdaten zu extrahieren. "
        #"Die Extraktion dieser Informationen ist von zentraler Bedeutung für die Erstellung automatisierter Unternehmensdatenbanken, rechtliche Dokumentationen und die Kontaktaufnahme. "
        #"Bitte gehe deshalb sorgfältig und gewissenhaft vor.\n\n"
        #"Analysiere den folgenden Textauszug einer Impressumsseite und extrahiere die darin enthaltenen Kontaktdaten:\n\n"
        #"{llm_text_input}\n\n"
        #"Gib die Daten ausschließlich im folgenden Format zurück:\n{extracted_data}\n"
        #"Wenn eine Angabe nicht direkt im Text steht, aber aus dem Kontext erschlossen werden kann, gib den wahrscheinlichsten Wert an. "
        #"Nur wenn absolut keine Information verfügbar oder ableitbar ist, verwende \"N/A\". "
        #"Gib ausschließlich die extrahierten Daten im genannten Format zurück – keine Kommentare, Erklärungen oder sonstige Ausgaben."

        #V3
        
        #"Du bist ein hochqualifizierter Experte für Datenextraktion und Textanalyse. "
        #"Deine Hauptaufgabe besteht darin, aus Impressums-Texten die wichtigsten rechtlich und geschäftlich relevanten Kontaktdaten strukturiert zu extrahieren. "
        #"Diese Daten sind essenziell für rechtliche Dokumentation, Geschäftsanalyse und automatisierte Verarbeitung.\n\n"

        #"Bitte extrahiere die folgenden Informationen:\n"
        #"{extracted_data}\n\n"

        #"Der folgende Text wurde von einer Impressumsseite extrahiert:\n\n"
        #"{llm_text_input}\n\n"

        #"Besonderheiten:\n"
        #"- Der Geschäftsführer bzw. die Geschäftsführerin kann in verschiedenen sprachlichen Varianten genannt sein, z. B. 'vertreten durch', 'in Person von', 'Managing Director', 'GF', 'CEO' oder 'geführt von'. "
        #"Berücksichtige alle Formulierungen, die auf eine verantwortliche geschäftsführende Person hinweisen.\n"
        #"- Achte bei Namensangaben auf Titel, mehrere Personen und ungewöhnliche Schreibweisen (z. B. mit Komma oder ohne).\n"
        #"- Wenn eine Information nicht eindeutig angegeben ist, aber logisch aus dem Kontext erschlossen werden kann, gib den wahrscheinlichsten Wert an. "
        #"Nur wenn absolut keine Angabe vorhanden oder ableitbar ist, schreibe \"N/A\".\n\n"

        #"Gib die Ergebnisse ausschließlich in diesem strukturierten Format zurück:\n{extracted_data}\n"
        #"Keine zusätzlichen Kommentare oder Erklärungen. Nur die Rohdaten."
        
        #v4
        "Du bist ein hochqualifizierter Experte für Datenextraktion und Textanalyse. "
        "Deine Aufgabe ist es, aus Impressums-Texten strukturierte, geschäftsrelevante Kontaktdaten zu extrahieren. "
        "Diese Daten sind entscheidend für rechtliche Dokumentationen, Recherchezwecke und die automatische Weiterverarbeitung in Unternehmensdatenbanken.\n\n"

        "Bitte extrahiere die folgenden Informationen:\n"
        "{extracted_data}\n\n"

        "Der folgende Text wurde von einer Impressumsseite extrahiert:\n\n"
        "{llm_text_input}\n\n"

        "Achte bei der Extraktion besonders auf die Nennung von geschäftsführenden oder vertretungsberechtigten Personen. "
        "Typische Hinweise darauf finden sich oft in Formulierungen, die folgende Begriffe enthalten:\n"
        "- 'Geschäftsführ', 'Geschäftsleit', 'Inhaber', 'Vertretungsberechtigt', 'vertreten', 'Inh.', 'Gf.', 'GF:', 'Verantwortlich'.\n"
        "Diese Begriffe können auch in unterschiedlichen Schreibweisen oder in Verbindung mit Namen oder Titeln auftreten. "
        "Beziehe alle relevanten Textstellen ein, auch wenn der Name nicht direkt nach dem Begriff steht oder in einer anderen grammatikalischen Form erscheint.\n\n"

        "Wenn eine Information nicht direkt genannt ist, aber mit hoher Wahrscheinlichkeit aus dem Kontext erschlossen werden kann, gib den plausibelsten Wert an. "
        "Nur wenn keine sinnvolle Ableitung möglich ist, schreibe \"N/A\".\n\n"

        "Gib ausschließlich die extrahierten Daten im folgenden Format zurück:\n{extracted_data}\n"
        "Keine zusätzlichen Kommentare oder Erklärungen. Nur die Rohdaten im genannten Format."

    )

    # Prompt füllen
    prompt = prompt_template.format(
        llm_text_input=llm_text_input,
        extracted_data=extracted_data
    )

    # Chat-Stream starten
    stream = chat(
        model='deepseek-r1:32b',
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

    clean_output = re.sub(r'<think>.*?</think>', '', buffer, flags=re.DOTALL)

    return clean_output.strip()