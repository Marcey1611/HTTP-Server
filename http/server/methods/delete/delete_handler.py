import re

from entity.models import Response, Request
from data.json import json_handler

def handle_delete(request: Request) -> Response:

    if "/json" in request.path:
        pattern = "^/json/delete_user\?name=[^&]+$"
        if re.match(pattern, request.path):
            query = request.path.split("?")[1]
            json_handler.delete_name(query)
        body = "User sucessfully deleted."
        return Response("HTTP/1.1 200 OK", "text/plain", body, len(body))
    else:
        return Response("HTTP/1.1 404 Not Found", "text/plain", "404 Not Found", len("404 Not Found"))


#regex für später: ^/json/delete_user\?(username=[^&]+(&age=[0-9]+(<=|>=|<|>)?[0-9]+)?)?(&age=[0-9]+(<=|>=|<|>)?[0-9]+)?$
