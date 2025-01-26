import logging
import base64
import os
import json

from entity.models import Request
from entity import validation_set
from entity.exceptions import NotFoundException, MethodNotAllowedException, BadRequestException, UnsupportedMediaTypeException, NotAcceptableException, NotImplementedException, LengthRequiredException, UnauthorizedException, ForbiddenException, HTTPVersionNotSupportedException

auth_path = os.getcwd() + "/auth.json"

def unpack_request(raw_request):
    method = None
    path = None
    headers = None
    body = None
    query = None

    try:
        method, path, version = raw_request.split(" ")[0], raw_request.split(" ")[1], raw_request.split(" ")[2]
        if "HTTP/1.1" not in version:
            raise HTTPVersionNotSupportedException("Invalid HTTP version. This server just supports HTTP/1.1")
        if "?" in path:
            query = path.split("?")[1]
            path = path.split("?")[0]
        if "\r\n\r\n" in raw_request:
            header_part = raw_request.split("\r\n\r\n", 1)[0]
            body = raw_request.split("\r\n\r\n", 1)[1]
        else:
            header_part = raw_request
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
            if key in headers:
                raise BadRequestException("Duplicate header(s).")
            values = [v.split(";")[0].strip() for v in value.split(",")]
            headers[key] = values

        return headers
    except BadRequestException as e:
        logging.error(e)
        raise e
    except Exception as e:
        logging.error(e)
        raise e
    
def validate_request(path, method, headers, body, query, host, host_ip, port):
    try:
        if path not in validation_set.set:
            raise NotFoundException("Path not found.")
        route = validation_set.set.get(path)
        if method not in route:
            allowed_methods = list(route.keys())
            raise MethodNotAllowedException(allowed_methods, "Method not allowed.")
        route_method = route[method]

        validate_authorization(route_method, headers, method)
        validate_headers(route_method, headers, host, host_ip, port, body)
            
        if route_method["body_required"] and not body:
            raise BadRequestException("Missing required body.")
        if route_method["query_required"] and not query:
            raise BadRequestException("Missing required query.")
        if not route_method["query_allowed"] and query:
            raise BadRequestException("Query not allowed.")
        
        if "handler" not in route_method:
            raise NotImplementedException("Ressource not implemented yet.")
        else:
            handler = route_method["handler"]

        return Request(path, method, headers, handler, body, query)
    except Exception as e:
        logging.error(e)
        raise e
    
def validate_authorization(route_method, headers, method):
    if "auth_required" in route_method and route_method["auth_required"]:
        if "authorization" not in headers:
            raise UnauthorizedException("Missing authorization.")
        try:

            base64_credentials = headers["authorization"][0][6:].strip()
            username, password_hash = base64.b64decode(base64_credentials).decode().split(":", 1)

            with open(auth_path, "r") as f:
                data = json.load(f)

            authenticated = False
            for user in data.get("users", []):
                if user["name"] == username and user["password"] == password_hash:
                    if method not in user["allowed_to"]:
                        raise ForbiddenException("No permission for this operation.")
                    authenticated = True
                    break
            if not authenticated:
                raise UnauthorizedException("No authorization.")
        except ForbiddenException as e:
            logging.error(e)
            raise e
        except UnauthorizedException as e:
            logging.error(e)
            raise e
        except Exception as e:
            logging.error(e)
            raise UnauthorizedException("Invalid authorization.")
        
def validate_headers(route_method, headers, host, host_ip, port, body):
    required_headers = route_method["required_headers"]

    for header, values in required_headers.items():
        if header not in headers:
            if header == "content-length":
                raise LengthRequiredException("Missing content-length header.")
            raise BadRequestException(f"Missing required header(s): {header}")
        
        if header == "host":
            if headers["host"][0] != f"{host}:{port}" and headers["host"][0] != f"{host_ip}:{port}":
                raise NotFoundException("Invalid host header.")
        
        if header == "content-type" and headers["content-type"][0] not in values:
            raise UnsupportedMediaTypeException("Unsupported media type.")

        if header == "content-length" and "content-length" not in headers:
            raise BadRequestException("Invalid content-length.")

    if "content-length" in headers and len(body.encode("utf-8")) != int(headers["content-length"][0]):
            raise BadRequestException("Invalid content-length.")

    if "accept" in headers:
        acceptable = False
        for accept in route_method["accept"]:
            if accept in headers["accept"]:
                acceptable = True
                break
        if not acceptable:
            raise NotAcceptableException("Accept header contains no supported content-type.")