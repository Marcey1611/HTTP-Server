import os
import xml.etree.ElementTree as ET
import logging

from entity.models import Response, Request
from entity.enums import HttpStatus, ContentType
from entity.exceptions import UnprocessableEntityException

file_path = os.getcwd() + "/handler/divs/data.html"

def get_divs(request: Request) -> Response:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()
        headers = {}
        headers["Content-Type"] = ContentType.HTML.value
        return Response(HttpStatus.OK.value, headers, data)
    except Exception as e:
        raise e
    
def post_divs(request: Request) -> Response:
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        body = root.find("body")
        if body is None:
            raise Exception # Ist ein 500er
        try:
            new_data = ET.fromstring(request.body)
        except ET.ParseError:
            raise UnprocessableEntityException("Invalid html.")

        if new_data.tag.lower() != "div":
            raise UnprocessableEntityException("Invalid html.")

        body.append(new_data)
        tree.write(file_path, encoding="unicode", method="html")

        body = "Div successfully created!"
        headers = {}
        headers["Content-Type"] = ContentType.PLAIN.value
        return Response(HttpStatus.OK.value, headers, body)
    except UnprocessableEntityException as exception:
        raise exception
    except Exception as e:
        logging.error(e)
        raise e
    
    
