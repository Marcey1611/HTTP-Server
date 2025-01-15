import os
import xml.etree.ElementTree as ET

file_path = "/data/html/data.html"

def get_data() -> str:
    try:
        # Datei öffnen und Inhalt lesen
        with open(os.getcwd() + file_path, "r", encoding="utf-8") as file:
            data = file.read()
        return data
    except Exception as e:
        raise e
    
def add_data(data):
    # HTML-Datei laden
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Das <body>-Tag finden
    body = root.find("body")
    if body is None:
        raise ValueError("Die HTML-Datei enthält kein <body>-Tag.")

    # Neues HTML-Element hinzufügen
    new_data = ET.fromstring(data)
    body.append(new_data)

    # Änderungen in der HTML-Datei speichern
    tree.write(file_path, encoding="unicode", method="html")
