from dataclasses import dataclass
from typing import Callable, Optional

@dataclass
class Request:
    path: str
    method: str
    headers: dict
    handler: Callable
    body: Optional[str] = None
    query: Optional[str] = None
    

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