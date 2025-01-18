import os
import xml.etree.ElementTree as ET
import logging

from entity.models import Response, Request
from entity.enums import HttpStatus, ContentType

file_path = os.getcwd() + "/handler/divs/data.html"

def get_divs(request: Request) -> Response:
    try:
        # Datei öffnen und Inhalt lesen
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()
        return Response("HTTP/1.1 "+HttpStatus.OK.value, ContentType.HTML.value, data, len(data))
    except Exception as e:
        raise e
    
def post_divs(request: Request) -> Response:
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        body = root.find("body")
        if body is None:
            raise Exception # Ist ein 500er

        new_data = ET.fromstring(request.body)

        if new_data.tag.lower() != "div":
            raise Exception()

        body.append(new_data)
        tree.write(file_path, encoding="unicode", method="html")

        body = "Div successfully created!"
        return Response("HTTP/1.1 "+HttpStatus.OK.value, ContentType.PLAIN.value, body, len(body))
    except Exception as e:
        logging.error(e)
        raise e
    
    
