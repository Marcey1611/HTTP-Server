import logging

from entity.models import Request
from entity import validation_set
from entity.exceptions import NotFoundException, MethodNotAllowedException, BadRequestException, UnsupportedMediaTypeException, NotAcceptableException, NotImplementedException, LengthRequiredException


def unpack_request(raw_request):
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
        return path, method, headers, body, query
    except Exception as e:
        logging.error(e)
        raise e

def parse_headers(header_part):
    try:
        lines = header_part.split("\r\n")[1:]
        headers = {}

        for line in lines:
            if ":" not in line:
                raise BadRequestException()
            key, value = line.split(":", 1)
            key = key.strip().lower()
            values = [v.split(";")[0].strip() for v in value.split(",")]
            headers[key] = values

        return headers
    except Exception as e:
        logging.error(e)
        raise e

    
def validate_request(path, method, headers, body, query):
    try:
        if path not in validation_set.set:
            raise NotFoundException("Path not found.")
        route = validation_set.set.get(path)
        if method not in route:
            allowed_methods = list(route.keys())
            raise MethodNotAllowedException(allowed_methods, "Method not allowed.")
        route_method = route[method]

        required_headers = route_method["required_headers"]

        for header, values in required_headers.items():
            if header not in headers:
                if header == "content-length":
                    raise LengthRequiredException("Missing content-length header.")
                raise BadRequestException(f"Missing required header(s): {header}")
            
            if header == "host":
                if headers["host"][0] not in values:
                    raise NotFoundException("Invalid host header.")
            
            if header == "content-type" and headers["content-type"][0] not in values:
                raise UnsupportedMediaTypeException("Unsupported media type.")
            
            if header == "content-length" and len(body) != int(headers["content-length"][0]):
                raise BadRequestException("Invalid content-length.")
            
        if route_method["body_required"] and not body:
            raise BadRequestException("Missing required body.")
        if route_method["query_required"] and not query:
            raise BadRequestException("Missing required query.")
        if not route_method["query_allowed"] and query:
            raise BadRequestException("Query not allowed.")
        
        if "accept" in headers:
            acceptable = False
            for accept in route_method["accept"]:
                if accept in headers["accept"]:
                    acceptable = True
                    break
            if not acceptable:
                raise NotAcceptableException("Accept header contains no supported content-type.")
        
        if "handler" not in route_method:
            raise NotImplementedException("Ressource not implemented yet.")
        else:
            handler = route_method["handler"]

        return Request(path, method, headers, handler, body, query)
    except Exception as e:
        logging.error(e)
        raise e