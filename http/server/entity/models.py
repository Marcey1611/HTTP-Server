from dataclasses import dataclass
from typing import Callable, Optional
from datetime import datetime, timezone

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
    headers: dict
    body: str

    def build_http_response(self) -> str:
        content_length = len(self.body)
        self.headers["Content-Length"] = content_length
        current_time = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
        self.headers["Date"] = current_time
        response_line = f"HTTP/1.1 {self.status}"
        headers_str = "\r\n".join(f"{key}: {value}" for key, value in self.headers.items())
        http_response = f"{response_line}\r\n{headers_str}\r\n\r\n{self.body}"
        return http_response

@dataclass
class KeepAliveData:
    keep_alive_timeout: int
    max_requests: int
    request_count: int