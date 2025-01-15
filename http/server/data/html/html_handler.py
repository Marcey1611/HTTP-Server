import os
import xml.etree.ElementTree as ET
import logging

file_path = os.getcwd() + "/data/html/data.html"

def get_data() -> str:
    try:
        # Datei öffnen und Inhalt lesen
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()
        return data
    except Exception as e:
        raise e
    
def add_data(data):
    try:
        # HTML-Datei laden
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Das <body>-Tag finden
        body = root.find("body")
        if body is None:
            raise Exception # Ist ein 500er

        # Neues HTML-Element erstellen
        new_data = ET.fromstring(data)

        # Überprüfen, ob das Element ein <div>-Tag ist
        if new_data.tag.lower() != "div":
            raise ValueError()

        # Neues <div>-Element zum <body> hinzufügen
        body.append(new_data)

        # Änderungen in der HTML-Datei speichern
        tree.write(file_path, encoding="unicode", method="html")
    except ValueError as e:
        logging.error(e)
        raise e
    except Exception as e:
        logging.error(e)
        raise e
    
    
