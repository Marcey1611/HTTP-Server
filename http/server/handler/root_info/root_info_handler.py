import os
import logging

from entity.models import Request, Response
from entity.enums import HttpStatus, ContentType
from handler.root_info import markdown_to_html_converter

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