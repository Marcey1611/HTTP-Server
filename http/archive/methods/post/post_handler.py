import json
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
import logging

#from data.json import json_handler
#from data.xml import xml_handler
#from data.html import html_handler
from entity.models import Request, Response

def handle_post(request: Request) -> Response:
    try:
        if request.path == "/json/add_user":
            if request.headers["content-type"] != "application/json":
                body = "415 Unsupported Content-Type"
                return Response("HTTP/1.1 "+body, "text/plain", body, len(body))
            try:
                # Übergib die JSON-Daten an die Methode
                #json_handler.add_new_user(request.body)
                
                # Erfolgsantwort zurückgeben
                body = "Data submitted"
                return Response("HTTP/1.1 201 Created", "text/plain", body, len(body))
            except json.JSONDecodeError as e:
                # Fehler bei der JSON-Verarbeitung
                body = "422 Unprocessable Entity"
                return Response("HTTP/1.1 "+body, "text/plain", body, len(body))
            
        if request.path == "/xml/add_new_product":
            if request.headers["content-type"] != "application/xml":
                body = "415 Unsupported Content-Type"
                return Response("HTTP/1.1 "+body, "text/plain", body, len(body))
            try:
                #xml_handler.add_new_product(request.body)

                # Erfolgsantwort zurückgeben
                body = "Data submitted"
                return Response("HTTP/1.1 201 Created", "text/plain", body, len(body))
            except ET.ParseError:
                # Fehler bei der XML-Verarbeitung
                body = "422 Unprocessable Entity"
                return Response("HTTP/1.1 "+body, "text/plain", body, len(body))
                
        if request.path == "/html/add_data":
            if request.headers["content-type"] != "text/html":
                body = "415 Unsupported Content-Type"
                return Response("HTTP/1.1 "+body, "text/plain", body, len(body))
            try:
                #html_handler.add_data(request.body)

                # Erfolgsantwort zurückgeben
                body = "Data submitted"
                return Response("HTTP/1.1 201 Created", "text/plain", body, len(body))
            except ValueError as e:
                body = ": Es sind nur div-Elemente erlaubt!"
                status = "422 Unprocessable Entity"
                return Response("HTTP/1.1 "+status, "text/plain", status+body, len(status+body))
            except ET.ParseError:
                # Fehler bei der XML-Verarbeitung
                body = "422 Unprocessable Entity"
                return Response("HTTP/1.1 "+body, "text/plain", body, len(body))
            
        else:
            # Pfad nicht gefunden
            body = "404 Not Found"
            return Response("HTTP/1.1 "+body, "text/plain", body, len(body))
    except Exception as e:
        logging.error(e)
        raise e