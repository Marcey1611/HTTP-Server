import os
import xml.etree.ElementTree as ET
import logging

from entity.models import Response, Request

file_path = os.getcwd() + "/handler/divs/data.html"

def get_divs(request: Request) -> str:
    try:
        # Datei öffnen und Inhalt lesen
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()
        return Response("HTTP/1.1 200 OK", "text/html", data, len(data))
    except Exception as e:
        raise e
    
def post_divs(request: Request):
    try:
        # HTML-Datei laden
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Das <body>-Tag finden
        body = root.find("body")
        if body is None:
            raise Exception # Ist ein 500er

        # Neues HTML-Element erstellen
        new_data = ET.fromstring(request.data)

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
    
    
