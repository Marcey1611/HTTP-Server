import json
import os
import logging

# Datei-Pfad zur JSON-Datei
file_path = os.getcwd() + '/data/json/data.json'

def get_data():
    try:
        # Datei öffnen und Inhalt lesen
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()
        return data
    except Exception as e:
        raise e


def add_new_user(new_user):
    try:
        # JSON-File einlesen
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)  # Bestehendes JSON-Objekt laden
        except FileNotFoundError:
            # Falls Datei nicht existiert, neues JSON-Objekt erstellen
            data = {"users": []}

        # JSON-String in ein Python-Objekt umwandeln
        new_data = json.loads(new_user)

        # Neuen Benutzer hinzufügen
        data["users"].append(new_data)

        # Aktualisiertes JSON-Objekt zurück in die Datei schreiben
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)  # Schön formatieren mit Einrückung
    except Exception as e:
        logging.error(e)
        raise e

def delete_name(query):
    name = query.split("=")[1]
    try:
        # JSON-Daten aus der Datei lesen
        with open(file_path, "r") as file:
            json_data = json.load(file)

        # Überprüfen, ob 'users' im JSON vorhanden ist
        if 'users' not in json_data:
            logging.error("Kein useres in datei")
            raise Exception # 500er

        # Filtere die Benutzer, um nur die zu behalten, deren Name nicht dem zu löschenden Namen entspricht
        json_data['users'] = [user for user in json_data['users'] if user['name'] != name]

        # Geänderte Daten in die Datei zurückschreiben
        with open(file_path, "w") as file:
            json.dump(json_data, file, indent=4)

    except Exception as e:
        logging.error(e)
        raise e
