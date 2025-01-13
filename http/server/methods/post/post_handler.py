import json
import logging

from data.json import json_handler

def handle_post(path, body, content_type):
    try:
        if path == "/json/add_user":
            if content_type != "application/json":
                return "HTTP/1.1 415 Unsupported Content-Type", "text/plain", "415 Unsupported Content-Type", len("415 Unsupported Content-Type")
            try:
                # Übergib die JSON-Daten an die Methode
                json_handler.add_new_user(body)
                
                # Erfolgsantwort zurückgeben
                return "HTTP/1.1 201 Created", "text/plain", "Data submitted", len("Data submitted")
            except json.JSONDecodeError as e:
                logging.error(e)
                # Fehler bei der JSON-Verarbeitung
                error_message = "Invalid JSON format"
                return "HTTP/1.1 422 Unprocessable Entity", "text/plain", error_message, len(error_message)
        else:
            # Pfad nicht gefunden
            return "HTTP/1.1 404 Not Found", "text/plain", "404 Not Found", len("404 Not Found")
    except Exception as e:
        raise e