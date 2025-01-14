from dataclasses import dataclass

@dataclass
class Request:
    method: str
    path: str
    headers: dict
    body: str = None

@dataclass
class Response:
    status: str
    content_type: str
    body: str
    content_length: int
    connection: str = None

@dataclass
class KeepAliveData:
    keep_alive_timeout: int
    max_requests: int
    request_count: int