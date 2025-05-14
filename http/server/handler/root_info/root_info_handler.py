import os
import json
import logging
from typing import Any

from entity.models import Request, Response
from entity.enums import HttpStatus, ContentType
from handler.root_info import markdown_to_html_converter
from entity import validation_set

# Pfade für wichtige Dateien
readme_file_path = os.getcwd() + "/../../README.md"  # Pfad zur README-Datei
root_file_path = os.getcwd() + "/handler/root_info/root.html"  # Pfad zur Root-HTML-Datei

def get_root(request: Request) -> Response:
    """
    Verarbeitet eine GET-Anfrage, um die Root-HTML-Datei zurückzugeben.
    """
    try:
        # Öffne die Root-HTML-Datei und lese ihren Inhalt
        with open(root_file_path, "r", encoding="utf-8") as file:
            data = file.read()

        # Setze den Content-Type auf HTML
        headers = {}
        headers["Content-Type"] = ContentType.HTML.value

        # Rückgabe der HTTP-Antwort mit HTML-Daten
        return Response(HttpStatus.OK.value, headers, data)
    except Exception as e:
        logging.error(f"Fehler beim Lesen der Root-HTML-Datei: {e}")
        raise e

def get_info(request: Request) -> Response:
    """
    Verarbeitet eine GET-Anfrage, um die README-Datei als HTML zurückzugeben.
    """
    try:
        # Öffne die README-Datei und lese ihren Inhalt
        with open(readme_file_path, "r", encoding="utf-8") as file:
            data = file.read()

        # Konvertiere den Markdown-Inhalt der README in HTML
        body = markdown_to_html_converter.generate_full_html(data)

        # Setze den Content-Type auf HTML
        headers = {}
        headers["Content-Type"] = ContentType.HTML.value

        # Rückgabe der HTTP-Antwort mit HTML-Daten
        return Response(HttpStatus.OK.value, headers, body)
    except Exception as e:
        logging.error(f"Fehler beim Verarbeiten der README-Datei: {e}")
        raise e

def get_config(request: Request) -> Response:
    """
    Verarbeitet eine GET-Anfrage, um die Server-Konfiguration (Validation Set) zurückzugeben.
    """
    try:
        # Transformiere die Datenstruktur aus dem Validation Set in eine serialisierbare Form
        transformed_set = transform_data(validation_set.set)

        # Serialisiere die Daten als JSON
        data = json.dumps(transformed_set, indent=4)

        # Setze den Content-Type auf JSON
        headers = {'Content-Type': ContentType.JSON.value}

        # Rückgabe der HTTP-Antwort mit den Konfigurationsdaten
        return Response(HttpStatus.OK.value, headers, data)
    except Exception as e:
        logging.error(f"Fehler beim Verarbeiten der Konfigurationsdaten: {e}")
        raise e

def transform_data(data: Any) -> Any:
    """
    Transformiert die Datenstruktur so, dass sie JSON-kompatibel wird:
    - Funktionen werden durch ihre Namen ersetzt.
    - Verschachtelte Strukturen werden rekursiv verarbeitet.
    """
    if isinstance(data, dict):
        # Rekursive Verarbeitung für Wörterbücher
        return {key: transform_data(value) for key, value in data.items()}
    elif callable(data):
        # Funktionen werden durch ihre Namen ersetzt
        return data.__name__
    elif isinstance(data, list):
        # Rekursive Verarbeitung für Listen
        return [transform_data(item) for item in data]
    else:
        # Andere Datentypen werden unverändert zurückgegeben
        return data
