import logging
import base64
import os
import json

from entity.models import Request
from entity import validation_set
from entity.exceptions import (NotFoundException, MethodNotAllowedException, BadRequestException,
                               UnsupportedMediaTypeException, NotAcceptableException, NotImplementedException,
                               LengthRequiredException, UnauthorizedException, ForbiddenException,
                               HTTPVersionNotSupportedException)

# Pfad zur JSON-Datei mit Benutzerinformationen für die Autorisierung
auth_path = os.getcwd() + "/auth.json"

def unpack_request(raw_request):
    """
    Parst eine rohe HTTP-Anfrage in ihre Bestandteile:
    Methode, Pfad, Header, Body und Query-Parameter.
    """
    method = None
    path = None
    headers = None
    body = None
    query = None

    try:
        # Zerlege die Anfrage in Methode, Pfad und HTTP-Version
        method, path, version = raw_request.split(" ")[0], raw_request.split(" ")[1], raw_request.split(" ")[2]

        # Überprüfe die unterstützte HTTP-Version
        if "HTTP/1.1" not in version:
            raise HTTPVersionNotSupportedException("Invalid HTTP version. This server just supports HTTP/1.1")
        
        # Extrahiere Query-Parameter aus dem Pfad (falls vorhanden)
        if "?" in path:
            query = path.split("?")[1]
            path = path.split("?")[0]
        
        # Teile Header und Body auf
        if "\r\n\r\n" in raw_request:
            header_part = raw_request.split("\r\n\r\n", 1)[0]
            body = raw_request.split("\r\n\r\n", 1)[1]
        else:
            header_part = raw_request
        
        # Header parsen
        headers = parse_headers(header_part)
        return path, method, headers, body, query
    except Exception as e:
        logging.error(e)
        raise e

def parse_headers(header_part):
    """
    Parst die HTTP-Header aus dem Header-Bereich der Anfrage.
    """
    try:
        lines = header_part.split("\r\n")[1:]  # Überspringe die erste Zeile (Request-Line)
        headers = {}

        for line in lines:
            # Überprüfe die Syntax jeder Header-Zeile
            if ":" not in line:
                raise BadRequestException("Ungültige Header-Zeile.")

            # Zerlege Header in Key und Value
            key, value = line.split(":", 1)
            key = key.strip().lower()

            # Prüfe auf doppelte Header (nicht erlaubt)
            if key in headers:
                raise BadRequestException("Duplicate header(s).")

            # Verarbeite mehrere Werte eines Headers
            values = [v.split(";")[0].strip() for v in value.split(",")]
            headers[key] = values

        return headers
    except BadRequestException as e:
        logging.error(e)
        raise e
    except Exception as e:
        logging.error(e)
        raise e

def validate_request(path, method, headers, body, query, host, host_ip, port):
    """
    Validiert die Anfrage anhand des vordefinierten `validation_set`.
    """
    try:
        # Überprüfe, ob der Pfad existiert
        if path not in validation_set.set:
            raise NotFoundException("Path not found.")
        
        route = validation_set.set.get(path)

        # Überprüfe, ob die HTTP-Methode für den Pfad erlaubt ist
        if method not in route:
            allowed_methods = list(route.keys())
            raise MethodNotAllowedException(allowed_methods, "Method not allowed.")
        
        route_method = route[method]

        # Validierung von Autorisierung und Headern
        validate_authorization(route_method, headers, method)
        validate_headers(route_method, headers, host, host_ip, port, body)
            
        # Überprüfe Anforderungen an Body und Query
        if route_method["body_required"] and not body:
            raise BadRequestException("Missing required body.")
        if route_method["query_required"] and not query:
            raise BadRequestException("Missing required query.")
        if not route_method["query_allowed"] and query:
            raise BadRequestException("Query not allowed.")
        
        # Überprüfe, ob ein Handler für den Pfad existiert
        if "handler" not in route_method:
            raise NotImplementedException("Resource not implemented yet.")
        else:
            handler = route_method["handler"]

        # Rückgabe der validierten Anfrage
        return Request(path, method, headers, handler, body, query)
    except Exception as e:
        logging.error(e)
        raise e

def validate_authorization(route_method, headers, method):
    """
    Validiert die Autorisierung basierend auf den Headern und den Benutzerdaten.
    """
    if "auth_required" in route_method and route_method["auth_required"]:
        # Überprüfe, ob der Authorization-Header vorhanden ist
        if "authorization" not in headers:
            raise UnauthorizedException("Missing authorization.")
        try:
            # Extrahiere Base64-encodierte Anmeldedaten
            base64_credentials = headers["authorization"][0][6:].strip()
            username, password_hash = base64.b64decode(base64_credentials).decode().split(":", 1)

            # Lade Benutzerdaten aus der JSON-Datei
            with open(auth_path, "r") as f:
                data = json.load(f)

            authenticated = False

            # Überprüfe die Anmeldedaten gegen die Benutzerliste
            for user in data.get("users", []):
                if user["name"] == username and user["password"] == password_hash:
                    # Überprüfe, ob die Methode erlaubt ist
                    if method not in user["allowed_to"]:
                        raise ForbiddenException("No permission for this operation.")
                    authenticated = True
                    break
            
            if not authenticated:
                raise UnauthorizedException("No authorization.")
        except ForbiddenException as e:
            logging.error(e)
            raise e
        except UnauthorizedException as e:
            logging.error(e)
            raise e
        except Exception as e:
            logging.error(e)
            raise UnauthorizedException("Invalid authorization.")

def validate_headers(route_method, headers, host, host_ip, port, body):
    """
    Validiert die Header basierend auf den Anforderungen des Endpunkts.
    """
    required_headers = route_method["required_headers"]

    for header, values in required_headers.items():
        # Überprüfe, ob ein erforderlicher Header fehlt
        if header not in headers:
            if header == "content-length":
                raise LengthRequiredException("Missing content-length header.")
            raise BadRequestException(f"Missing required header(s): {header}")
        
        # Validierung des Host-Headers
        if header == "host":
            if headers["host"][0] != f"{host}:{port}" and headers["host"][0] != f"{host_ip}:{port}":
                raise NotFoundException("Invalid host header.")
        
        # Validierung des Content-Type-Headers
        if header == "content-type" and headers["content-type"][0] not in values:
            raise UnsupportedMediaTypeException("Unsupported media type.")

        # Validierung des Content-Length-Headers
        if header == "content-length" and "content-length" not in headers:
            raise BadRequestException("Invalid content-length.")

    # Überprüfe, ob die Content-Length mit der Body-Länge übereinstimmt
    if "content-length" in headers and len(body.encode("utf-8")) != int(headers["content-length"][0]):
        raise BadRequestException("Invalid content-length.")

    # Validierung des Accept-Headers
    if "accept" in headers:
        acceptable = False
        for accept in route_method["accept"]:
            if accept in headers["accept"]:
                acceptable = True
                break
        if not acceptable:
            raise NotAcceptableException("Accept header contains no supported content-type.")