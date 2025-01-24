import os
import json
import logging
from typing import Any

from entity.models import Request, Response
from entity.enums import HttpStatus, ContentType
from handler.root_info import markdown_to_html_converter
from entity import validation_set

readme_file_path = os.getcwd() + "/../../README.md"
root_file_path = os.getcwd() + "/handler/root_info/root.html"

def get_root(request: Request) -> Response:
    try:
        with open(root_file_path, "r", encoding="utf-8") as file:
            data = file.read()
        headers = {}
        headers["Content-Type"] = ContentType.HTML.value
        return Response(HttpStatus.OK.value, headers, data)
    except Exception as e:
        raise e

def get_info(request: Request) -> Response:
    try:
        with open(readme_file_path, "r", encoding="utf-8") as file:
            data = file.read()
        body = markdown_to_html_converter.generate_full_html(data)
        headers = {}
        headers["Content-Type"] = ContentType.HTML.value
        return Response(HttpStatus.OK.value, headers, body)
    except Exception as e:
        raise e
    
# Anpassung der `get_config`-Funktion
def get_config(request: Request) -> Response:
    try:
        # Transformation des verschachtelten Dictionaries
        transformed_set = transform_data(validation_set.set)
        
        # JSON serialisieren
        data = json.dumps(transformed_set, indent=4)
        
        # Headers setzen
        headers = {'Content-Type': ContentType.JSON.value}
        return Response(HttpStatus.OK.value, headers, data)
    except Exception as e:
        logging.error(e)
        raise e
    
def transform_data(data: Any) -> Any:
    if isinstance(data, dict):
        # Falls es ein Dictionary ist, wandle alle Werte rekursiv um
        return {key: transform_data(value) for key, value in data.items()}
    elif callable(data):
        # Falls es eine Funktion ist, gib ihren Namen zurück
        return data.__name__
    elif isinstance(data, list):
        # Falls es eine Liste ist, wandle jedes Element rekursiv um
        return [transform_data(item) for item in data]
    else:
        # Andernfalls gib den Wert unverändert zurück
        return data