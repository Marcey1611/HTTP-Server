import logging

from entity.models import Request
from entity import validation_set
from entity.exceptions import NotFoundException, MethodNotAllowedException, BadRequestException, UnsupportedMediaTypeException, NotAcceptableException, NotImplementedException


def unpack_request(raw_request) -> Request:
    method = None
    path = None
    headers = None
    body = None
    query = None

    try:
        method, path, _ = raw_request.split(" ")[0], raw_request.split(" ")[1], raw_request.split(" ")[2]
        if "?" in path:
            query = path.split("?")[1]
            path = path.split("?")[0]
        # Header und Body trennen
        if "\r\n\r\n" in raw_request:
            header_part = raw_request.split("\r\n\r\n", 1)[0]
            body = raw_request.split("\r\n\r\n", 1)[1]
        else:
            header_part = raw_request  # Falls kein Body vorhanden ist, ist alles der Header
        headers = parse_headers(header_part)
        return validate_request(path, method, headers, body, query)
    except Exception as e:
        logging.error(e)
        raise e

def parse_headers(header_part):
    try:
        

        # Zeilen des Headers extrahieren (ohne Startzeile)
        lines = header_part.split("\r\n")[1:]  # Startzeile überspringen

        headers = {}
        for line in lines:
            if ":" not in line:
                logging.warning(f"Ungültiger Header: {line}")
                continue
            key, value = line.split(":", 1)
            headers[key.strip().lower()] = value.strip()  # Header in Kleinbuchstaben normalisieren

        return headers
    except Exception as e:
        logging.error(e)
        raise e
    
def validate_request(path, method, headers, body, query):
    if path not in validation_set.set:
        raise NotFoundException()
    route = validation_set.set.get(path)
    if method not in route:
        raise MethodNotAllowedException()
    route_method = route[method]

    required_headers = route_method["required_headers"]

    for header, values in required_headers.items():
        if header not in headers:
            raise BadRequestException()
        
        if header == "host" and headers["host"] not in values:
            raise NotFoundException()
        
        if header == "content-type" and headers["content-type"] not in values:
            raise UnsupportedMediaTypeException()
    
        
    if (route_method["body_required"] and not body) or (route_method["query_required"] and not query) or (route_method["query_allowed"] and query):
        raise BadRequestException()
    
    if "accept" in headers:
        for accept in headers["accept"]:
            if accept not in route_method["accept"]:
                raise NotAcceptableException()
    try:        
        if "handler" not in route_method:
            raise NotImplementedException()
        else:
            handler = route_method["handler"]
        
        return Request(path, method, headers, handler, body, query)
    except Exception as e:
        logging.error(e)
        raise e