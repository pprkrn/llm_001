import re
from ollama import chat
from webscrape_imprint import run_scraper

def extract_name_candidates(text):
    # Sucht Titel + Vorname + Nachname (auch ohne Titel)
    name_pattern = r'(?:Dr\.|Prof\.|Herr|Frau)?\s?[A-ZÄÖÜ][a-zäöüß]+\s+[A-ZÄÖÜ][a-zäöüß]+'
    matches = re.findall(name_pattern, text)
    return list(set([match.strip() for match in matches]))

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

    # Vorverarbeitung: Mögliche Namen erkennen
    name_candidates = extract_name_candidates(llm_text_input)
    name_hint = "\nErkannte mögliche Personennamen im Text:\n- " + "\n- ".join(name_candidates) if name_candidates else ""

    # Prompt bauen
    prompt_template = (
        "Du bist ein Experte für Datenextraktion aus juristischen Texten. "
        "Analysiere den folgenden Impressumstext und extrahiere strukturierte Kontaktdaten.\n\n"

        "Besonderes Augenmerk liegt auf der Identifikation von Personen in leitender Funktion, z. B. Geschäftsführer, Inhaber oder vertretungsberechtigte Personen. "
        "Folgende Namen wurden automatisch erkannt und könnten relevant sein:{name_hint}\n\n"

        "Beziehe diese Namen in deine Analyse ein und gib sie ggf. unter 'Geschäftsführer' an – aber nur, wenn aus dem Kontext hervorgeht, dass sie in entsprechender Funktion genannt sind.\n\n"

        "Wenn eine Information nicht vorhanden oder nicht ableitbar ist, schreibe \"N/A\".\n\n"
        
        "Textauszug:\n\n"
        "{llm_text_input}\n\n"

        "Gib ausschließlich die folgenden Daten im exakten Format zurück:\n"
        "{extracted_data}\n"
        "Keine Erklärungen oder Kommentare."
    )

    # Prompt einsetzen
    prompt = prompt_template.format(
        llm_text_input=llm_text_input,
        extracted_data=extracted_data,
        name_hint=name_hint
    )

    # LLM anfragen
    stream = chat(
        model='deepseek-r1:32b',
        messages=[{
            'role': 'user',
            'content': prompt,
        }],
        stream=True,
    )

    # Antwort sammeln
    buffer = ""
    for chunk in stream:
        content = chunk['message']['content']
        buffer += content

    clean_output = re.sub(r'<think>.*?</think>', '', buffer, flags=re.DOTALL)

    return clean_output.strip()