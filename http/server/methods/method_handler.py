import logging

from entity.models import Response, Request
from methods.get import get_handler
from methods.post import post_handler
from methods.delete import delete_handler

def handle_methods(raw_request, request: Request) -> Response:
    try:
        if request.method == "GET":
            if "accept" in request.headers:
                accept = request.headers["accept"]
            else:
                accept = None
            return get_handler.handle_get(request.path, accept)

        elif request.method == "POST":
            if "content-type" not in request.headers:
                body = "400 Bad Request"
                return Response("HTTP/1.1 "+body, "text/plain", body, len(body))
            else:
                request.body = raw_request.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in raw_request else ""
                logging.info(f"Body: {request.body}")
                
                return post_handler.handle_post(request)
        elif request.method == "DELETE":
            return delete_handler.handle_delete(request)
        else:
            status = "405 Method Not Allowed"
            return Response("HTTP/1.1 "+status, "text/plain", status, len(status))
    except Exception as e:
        logging.error(e)
        raise e