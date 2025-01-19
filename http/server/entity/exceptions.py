from entity.enums import HttpStatus, ContentType
from entity.models import Response

class NotAcceptableException(Exception):
    def __init__(self, message=HttpStatus.NOT_ACCEPTABLE.value):
        self.message = message
        headers = {}
        headers["Content-Type"] = ContentType.PLAIN.value
        self.response = Response(HttpStatus.NOT_ACCEPTABLE.value, headers, self.message)
        super().__init__(self.message)

class MethodNotAllowedException(Exception):
    def __init__(self, allowed_methods: list, message=HttpStatus.METHOD_NOT_ALLOWED.value):
        self.message = message
        headers = {}
        headers["Content-Type"] = ContentType.PLAIN.value
        headers["Allow"] = ", ".join(allowed_methods)
        self.response = Response(HttpStatus.METHOD_NOT_ALLOWED.value, headers, self.message)
        super().__init__(self.message)

class NotFoundException(Exception):
    def __init__(self, message=HttpStatus.NOT_FOUND.value):
        self.message = message
        headers = {}
        headers["Content-Type"] = ContentType.PLAIN.value
        self.response = Response(HttpStatus.NOT_FOUND.value, headers, self.message)
        super().__init__(self.message)

class BadRequestException(Exception):
    def __init__(self, message=HttpStatus.BAD_REQUEST.value):
        self.message = message
        headers = {}
        headers["Content-Type"] = ContentType.PLAIN.value
        self.response = Response(HttpStatus.BAD_REQUEST.value, headers, self.message)
        super().__init__(self.message)

class UnsupportedMediaTypeException(Exception):
    def __init__(self, message=HttpStatus.UNSUPPORTED_MEDIA_TYPE.value):
        self.message = message
        headers = {}
        headers["Content-Type"] = ContentType.PLAIN.value
        self.response = Response(HttpStatus.UNSUPPORTED_MEDIA_TYPE.value, headers, self.message)
        super().__init__(self.message)

class NotImplementedException(Exception):
    def __init__(self, message=HttpStatus.NOT_IMPLEMENTED.value):
        self.message = message
        headers = {}
        headers["Content-Type"] = ContentType.PLAIN.value
        self.response = Response(HttpStatus.NOT_IMPLEMENTED.value, headers, self.message)
        super().__init__(self.message)

class PayloadTooLargeException(Exception):
    def __init__(self, message=HttpStatus.PAYLOAD_TOO_LARGE.value):
        self.message = message
        headers = {}
        headers["Content-Type"] = ContentType.PLAIN.value
        self.response = Response(HttpStatus.PAYLOAD_TOO_LARGE.value, headers, self.message)
        super().__init__(self.message)

class LengthRequiredException(Exception):
    def __init__(self, message=HttpStatus.LENGTH_REQUIRED.value):
        self.message = message
        headers = {}
        headers["Content-Type"] = ContentType.PLAIN.value
        self.response = Response(HttpStatus.LENGTH_REQUIRED.value, headers, self.message)
        
        super().__init__(self.message)

class UnprocessableEntityException(Exception):
    def __init__(self, message=HttpStatus.UNPROCESSABLE_ENTITY.value):
        self.message = message
        headers = {}
        headers["Content-Type"] = ContentType.PLAIN.value
        self.response = Response(HttpStatus.UNPROCESSABLE_ENTITY.value, headers, self.message)
        super().__init__(self.message)

