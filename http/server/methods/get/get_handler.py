import logging

from data.html import html_handler
from data.json import json_handler
from data.xml import xml_handler

def handle_get(path):
    try: 
        if path == "/":
            data = "Hi, what's up. This is a example http server."
            return "HTTP/1.1 200 OK", "text/plain", data, len(data)
        elif path == "/info":
            data = "Some infos about this server..."
            return "HTTP/1.1 200 OK", "text/plain", data, len(data)
        elif path == "/json":
            data = json_handler.get_data()
            return "HTTP/1.1 200 OK", "application/json", data, len(data)
        elif path == "/html":
            data = html_handler.get_data()
            return "HTTP/1.1 200 OK", "text/html", data, len(data)
        elif path == "/xml":
            data = xml_handler.get_data()
            return "HTTP/1.1 200 OK", "application/xml", data, len(data)
        else:
            return "HTTP/1.1 404 Not Found", "text/plain", "404 Not Found", len("404 Not Found")
    except Exception as e:
        raise e
