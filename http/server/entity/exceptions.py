from entity.enums import HttpStatus, ContentType
from entity.models import Response

class NotAcceptableException(Exception):
    def __init__(self):
        self.message = HttpStatus.NOT_ACCEPTABLE.value
        self.response = Response("HTTP/1.1 "+self.message, ContentType.PLAIN.value, self.message, len(self.message), "close")
        super().__init__(self.message)

class MethodNotAllowedException(Exception):
    def __init__(self):
        self.message = HttpStatus.METHOD_NOT_ALLOWED.value
        self.response = Response("HTTP/1.1 "+self.message, ContentType.PLAIN.value, self.message, len(self.message), "close")
        super().__init__(self.message)

class NotFoundException(Exception):
    def __init__(self):
        self.message = HttpStatus.NOT_FOUND.value
        self.response = Response("HTTP/1.1 "+self.message, ContentType.PLAIN.value, self.message, len(self.message), "close")
        super().__init__(self.message)

class BadRequestException(Exception):
    def __init__(self):
        self.message = HttpStatus.BAD_REQUEST.value
        self.response = Response("HTTP/1.1 "+self.message, ContentType.PLAIN.value, self.message, len(self.message), "close")
        super().__init__(self.message)

class UnsupportedMediaTypeException(Exception):
    def __init__(self):
        self.message = HttpStatus.UNSUPPORTED_MEDIA_TYPE.value
        self.response = Response("HTTP/1.1 "+self.message, ContentType.PLAIN.value, self.message, len(self.message), "close")
        super().__init__(self.message)

class NotAcceptableException(Exception):
    def __init__(self):
        self.message = HttpStatus.NOT_ACCEPTABLE.value
        self.response = Response("HTTP/1.1 "+self.message, ContentType.PLAIN.value, self.message, len(self.message), "close")
        super().__init__(self.message)

class NotImplementedException(Exception):
    def __init__(self):
        self.message = HttpStatus.NOT_IMPLEMENTED.value
        self.response = Response("HTTP/1.1 "+self.message, ContentType.PLAIN.value, self.message, len(self.message), "close")
        super().__init__(self.message)

class PayloadTooLargeException(Exception):
    def __init__(self):
        self.message = HttpStatus.PAYLOAD_TOO_LARGE.value
        self.response = Response("HTTP/1.1 "+self.message, ContentType.PLAIN.value, self.message, len(self.message), "close")
        super().__init__(self.message)

