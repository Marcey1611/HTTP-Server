import json
import os
import logging
from typing import List

from entity.models import Response, Request
from entity.enums import HttpStatus, ContentType
from entity.exceptions import BadRequestException, UnprocessableEntityException

# Pfad zur JSON-Datei, die die Benutzerdaten enthält
file_path = os.getcwd() + '/handler/users/data.json'

def get_users(request: Request) -> Response:
    """
    Verarbeitet eine GET-Anfrage, um alle oder gefilterte Benutzer aus der JSON-Datei zurückzugeben.
    """
    try:
        # Öffne und lese die JSON-Datei
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Überprüfe, ob die Datei gültige Benutzerdaten enthält
        if 'users' not in data:
            logging.error("Benutzerdaten fehlen in der Datei.")
            raise Exception

        # Wenn Query-Parameter vorhanden sind, filtere die Benutzer
        if request.query:
            names, ages = parse_query(request.query)  # Query-Parameter extrahieren
            data = filter_in(data, names, ages)  # Benutzer filtern

        # Konvertiere die Daten in ein JSON-Format
        data = json.dumps(data, ensure_ascii=False, indent=4)
        headers = {}
        headers['Content-Type'] = ContentType.JSON.value

        # Rückgabe der Antwort mit den Benutzerdaten
        return Response(HttpStatus.OK.value, headers, data)
    except Exception as e:
        logging.error(e)
        raise e

def post_users(request: Request) -> Response:
    """
    Verarbeitet eine POST-Anfrage, um neue Benutzer zur JSON-Datei hinzuzufügen.
    """
    try:
        # Parse die Anfrage, um neue Benutzer zu extrahieren
        try:
            new_users = json.loads(request.body)
        except json.JSONDecodeError:
            raise UnprocessableEntityException("Invalid JSON.")
        
        # Lese die bestehende JSON-Datei
        with open(file_path, 'r', encoding="utf-8") as file:
            data = json.load(file)

        if 'users' not in data:
            logging.error("Benutzerdaten fehlen in der Datei.")
            raise Exception

        # Füge neue Benutzer hinzu (einzeln oder als Liste)
        if isinstance(new_users, list):
            for user in new_users:
                data["users"].append(user)
        else:
            data["users"].append(new_users)

        # Schreibe die aktualisierten Benutzerdaten zurück in die Datei
        with open(file_path, 'w', encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        # Erfolgsantwort erstellen
        body = "User(s) successfully created."
        headers = {}
        headers['Content-Type'] = ContentType.PLAIN.value
        return Response(HttpStatus.OK.value, headers, body)
    except UnprocessableEntityException as e:
        raise e
    except Exception as e:
        logging.error(e)
        raise e

def delete_users(request: Request) -> Response:
    """
    Verarbeitet eine DELETE-Anfrage, um Benutzer basierend auf Query-Parametern zu löschen.
    """
    try:
        # Lese die bestehende JSON-Datei
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if 'users' not in data:
            logging.error("Benutzerdaten fehlen in der Datei.")
            raise Exception

        # Extrahiere Query-Parameter und filtere Benutzer heraus
        names, ages = parse_query(request.query)
        filtered_users = filter_out(data, names, ages)

        # Aktualisiere die Benutzerdaten
        data["users"] = filtered_users

        # Schreibe die aktualisierten Daten in die Datei
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        # Erfolgsantwort erstellen
        body = "User(s) successfully deleted."
        headers = {}
        headers['Content-Type'] = ContentType.PLAIN.value
        return Response(HttpStatus.OK.value, headers, body)
    except Exception as e:
        logging.error(e)
        raise e

def put_users(request: Request) -> Response:
    """
    Verarbeitet eine PUT-Anfrage, um Benutzer zu aktualisieren oder hinzuzufügen.
    """
    try:
        # Parse die Anfrage, um die Benutzerinformationen zu extrahieren
        try:
            users = json.loads(request.body)
        except json.JSONDecodeError:
            raise UnprocessableEntityException("Invalid JSON.")

        # Lese die bestehende JSON-Datei
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if 'users' not in data:
            logging.error("Benutzerdaten fehlen in der Datei.")
            raise Exception

        # Aktualisiere existierende Benutzer oder füge neue hinzu
        for user in users:
            if not isinstance(user, dict) or "name" not in user or "age" not in user:
                raise BadRequestException()

            # Suche nach einem existierenden Benutzer
            existing_user = next((u for u in data["users"] if u["name"] == user["name"]), None)
            
            if existing_user:
                # Aktualisiere den Benutzer
                existing_user["age"] = user["age"]
            else:
                # Füge den Benutzer hinzu
                data["users"].append(user)
        
        # Schreibe die aktualisierten Benutzerdaten in die Datei
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        # Erfolgsantwort erstellen
        body = "User(s) successfully updated or added."
        headers = {}
        headers['Content-Type'] = ContentType.PLAIN.value
        return Response(HttpStatus.OK.value, headers, body)
    except UnprocessableEntityException as e:
        raise e        
    except Exception as e:
        logging.error(e)
        raise e

def parse_query(query: str) -> list:
    """
    Parst Query-Parameter, um Namen und Alter zu extrahieren.
    """
    try:
        queries = {}
        # Zerlege die Query-Parameter in Schlüssel-Wert-Paare
        for pair in query.split('&'):
            key, value = pair.split('=', 1)
            if key in queries:
                queries[key].append(value)
            else:
                queries[key] = [value]

        # Extrahiere Namen und Alter aus den Query-Parametern
        names = queries.get("name", [])
        ages = [int(age) for age in queries.get("age", [])]
        return names, ages
    except Exception as e:
        logging.error(e)
        raise e

def filter_in(data: json, names: List[str], ages: List[int]):
    """
    Filtert Benutzer, die den angegebenen Namen oder Alterskriterien entsprechen.
    """
    try:
        filtered_users = []
        for user in data.get("users"):
            if names and user.get("name") not in names:
                continue
            if ages and user.get("age") not in ages:
                continue
            filtered_users.append(user)
        return filtered_users
    except Exception as e:
        logging.error(e)
        raise e

def filter_out(data: json, names: List[str], ages: List[int]):
    """
    Entfernt Benutzer, die den angegebenen Namen oder Alterskriterien entsprechen.
    """
    try:
        filtered_users = []
        for user in data.get("users"):
            if names and user.get("name") in names:
                continue
            if ages and user.get("age") in ages:
                continue
            filtered_users.append(user)
        return filtered_users
    except Exception as e:
        logging.error(e)
        raise e
