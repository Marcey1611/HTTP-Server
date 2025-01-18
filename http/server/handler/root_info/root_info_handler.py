import os
import logging

from entity.models import Request, Response
from entity.enums import HttpStatus, ContentType
from handler.root_info import markdown_to_html_converter

file_path = os.getcwd() + "/../../README.md"

def get_root(request: Request) -> Response:
    try:
        body = "Hi, this is an exmaple http-server. To get more infos please call the /info interface."
        return Response("HTTP/1.1 "+HttpStatus.OK.value, ContentType.PLAIN.value, body, len(body))
    except Exception as e:
        logging.error(e)
        raise e

def get_info(request: Request) -> Response:
    try:
        # Datei öffnen und Inhalt lesen
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()
        body = markdown_to_html_converter.generate_full_html(data)
        return Response("HTTP/1.1 "+HttpStatus.OK.value, ContentType.HTML.value, body, len(body))
    except Exception as e:
        raise e