import os
import xml.etree.ElementTree as ET  # Zum Verarbeiten und Manipulieren von XML/HTML-Daten
import logging

from entity.models import Response, Request
from entity.enums import HttpStatus, ContentType
from entity.exceptions import UnprocessableEntityException

# Datei, in der die HTML-Daten gespeichert sind
file_path = os.getcwd() + "/handler/divs/data.html"

def get_divs(request: Request) -> Response:
    """
    Verarbeitet eine GET-Anfrage, um die gespeicherte HTML-Datei zurückzugeben.
    """
    try:
        # Öffne und lese die HTML-Datei
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()
        
        # Setze den Content-Type auf HTML
        headers = {}
        headers["Content-Type"] = ContentType.HTML.value
        
        # Rückgabe der Antwort mit dem HTML-Inhalt
        return Response(HttpStatus.OK.value, headers, data)
    except Exception as e:
        # Protokolliere Fehler und werfe sie erneut
        logging.error(e)
        raise e

def post_divs(request: Request) -> Response:
    """
    Verarbeitet eine POST-Anfrage, um ein neues `<div>`-Element in die HTML-Datei einzufügen.
    """
    try:
        # Parse die bestehende HTML-Datei
        tree = ET.parse(file_path)
        root = tree.getroot()  # Wurzelelement der HTML-Struktur

        # Suche das `<body>`-Element, wo das neue `<div>` hinzugefügt wird
        body = root.find("body")
        if body is None:
            # Wenn kein `<body>`-Tag vorhanden ist, liegt ein Fehler vor
            raise Exception
        
        try:
            # Parse den Body der Anfrage, um ein neues Element zu erstellen
            new_data = ET.fromstring(request.body)
        except ET.ParseError:
            # Wenn die HTML-Daten ungültig sind, werfe eine UnprocessableEntityException
            raise UnprocessableEntityException("Invalid html.")

        # Überprüfe, ob das neue Element ein `<div>` ist
        if new_data.tag.lower() != "div":
            raise UnprocessableEntityException("Invalid html.")

        # Füge das neue `<div>`-Element zum `<body>`-Tag hinzu
        body.append(new_data)
        
        # Schreibe die geänderte HTML-Struktur zurück in die Datei
        tree.write(file_path, encoding="unicode", method="html")

        # Erstelle die Antwort
        body = "Div successfully created!"
        headers = {}
        headers["Content-Type"] = ContentType.PLAIN.value  # Rückgabe als Plaintext
        return Response(HttpStatus.OK.value, headers, body)
    except UnprocessableEntityException as e:
        # Behandle ungültige Eingaben und werfe die entsprechende Ausnahme
        raise e
    except Exception as e:
        # Protokolliere allgemeine Fehler und werfe sie erneut
        logging.error(e)
        raise e
