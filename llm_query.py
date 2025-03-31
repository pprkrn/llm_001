from ollama import chat
from webscrape_imprint import text
import re

llm_text_input = text

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

# Chat-Stream starten
stream = chat(
    model='deepseek-r1:32b',
    messages=[{
        'role': 'user',
        'content': 'Stelle Kontaktdaten aus diesem Text ' + llm_text_input + ' in folgendem Format dar:' + extracted_data
    }],
    stream=True,
)

# Output ohne <think>...</think> ausgeben
buffer = ""

for chunk in stream:
    content = chunk['message']['content']
    buffer += content

# Entferne <think>...</think> aus dem gesamten Output
clean_output = re.sub(r'<think>.*?</think>', '', buffer, flags=re.DOTALL)

data_for_csv = clean_output.strip()

print(data_for_csv)