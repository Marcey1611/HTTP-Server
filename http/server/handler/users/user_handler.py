import json
import os
import logging

from entity.models import Response, Request
from entity.enums import HttpStatus, ContentType

# Datei-Pfad zur JSON-Datei
file_path = os.getcwd() + '/handler/users/data.json'

def get_users(request: Request) -> Response:
    try:
        # Datei öffnen und Inhalt lesen
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()
        return Response("HTTP/1.1 "+HttpStatus.OK.value, ContentType.JSON.value, data, len(data))
    except Exception as e:
        raise e


def post_users(request: Request) -> Response:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        new_data = json.loads(request.body)

        data["users"].append(new_data)

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        body = "User successfully created!"
        return Response("HTTP/1.1 "+HttpStatus.OK.value, ContentType.PLAIN.value, body, len(body))
    except Exception as e:
        logging.error(e)
        raise e

def delete_users(request: Request) -> Response:
    name = request.query.split("=")[1]
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

        body = "User successfully deleted!"
        return Response("HTTP/1.1 "+HttpStatus.OK.value, ContentType.PLAIN.value, body, len(body))
    except Exception as e:
        logging.error(e)
        raise e
