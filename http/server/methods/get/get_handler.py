import logging

from data.html import html_handler
from data.json import json_handler
from data.xml import xml_handler
from entity.models import Response

def handle_get(path, accept=None) -> Response:
    try: 
        if path == "/":
            if accept and "text/plain" not in accept:
                data = "406 Not Acceptable"
                return Response("HTTP/1.1 "+data, "text/plain", data, len(data))
            data = "Hi, what's up. This is a example http server."
            return Response("HTTP/1.1 200 OK", "text/plain", data, len(data))
        elif path == "/info":
            if accept and "text/plain" not in accept:
                data = "406 Not Acceptable"
                return Response("HTTP/1.1 "+data, "text/plain", data, len(data))
            data = "Some infos about this server..."
            return Response("HTTP/1.1 200 OK", "text/plain", data, len(data))
        elif path == "/json":
            if accept and "application/json" not in accept:
                data = "406 Not Acceptable"
                return Response("HTTP/1.1 "+data, "text/plain", data, len(data))
            data = json_handler.get_data()
            return Response("HTTP/1.1 200 OK", "application/json", data, len(data))
        elif path == "/html":
            if accept and "text/html" not in accept:
                data = "406 Not Acceptable"
                return Response("HTTP/1.1 "+data, "text/plain", data, len(data))
            data = html_handler.get_data()
            return Response("HTTP/1.1 200 OK", "text/html", data, len(data))
        elif path == "/xml":
            if accept and "application/xml" not in accept:
                data = "406 Not Acceptable"
                return Response("HTTP/1.1 "+data, "text/plain", data, len(data))
            data = xml_handler.get_data()
            return Response("HTTP/1.1 200 OK", "application/xml", data, len(data))
        else:
            return Response("HTTP/1.1 404 Not Found", "text/plain", "404 Not Found", len("404 Not Found"))
    except Exception as e:
        logging.error(e)
        raise e
