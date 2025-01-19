from enum import Enum

class HttpStatus(Enum):
    OK = "200 OK"
    BAD_REQUEST = "400 Bad Request"
    NOT_FOUND = "404 Not Found"
    METHOD_NOT_ALLOWED = "405 Method Not Allowed"
    NOT_ACCEPTABLE = "406 Not Acceptable"
    LENGTH_REQUIRED = "411 Length Required"
    PAYLOAD_TOO_LARGE = "413 Payload Too Large"
    UNSUPPORTED_MEDIA_TYPE = "415 Unsupported Media Type"
    UNPROCESSABLE_ENTITY = "422 Unprocessable Entity"
    INTERNAL_SERVER_ERROR = "500 Internal Server Error"
    NOT_IMPLEMENTED = "501 Not Implemented"

class ContentType(Enum):
    PLAIN = "text/plain"
    JSON = "application/json"
    HTML = "text/html"
    XML = "application/xml"
    ALL = "*/*"

class Method(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
