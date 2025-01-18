import logging

#from data.html import html_handler
#from data.json import json_handler
#from data.xml import xml_handler
from entity.models import Response, Request
from entity.exceptions import NotAcceptableException
from entity.enums import HttpStatus, ContentType

paths = ["/", "/info", "/json", "/xml", "/html"]

def handle_get(request: Request) -> Response:
    try: 
        
        if request.path == "/":
            check_accept_header(request, ContentType.PLAIN.value)
            data = "Hi, what's up. This is a example http server."
            return Response("HTTP/1.1 "+HttpStatus.OK.value, ContentType.PLAIN.value, data, len(data))
        
        elif request.path == "/info":
            check_accept_header(request, ContentType.PLAIN.value)
            data = "Some infos about this server..."
            return Response("HTTP/1.1 "+HttpStatus.OK.value, ContentType.PLAIN.value, data, len(data))
        
        elif request.path == "/json":
            check_accept_header(request, ContentType.JSON.value)
            #return json_handler.get_data()
                
        elif request.path == "/html":
            check_accept_header(request, ContentType.HTML.value)
            #return html_handler.get_data()
        
        elif request.path == "/xml":
            check_accept_header(request, ContentType.XML.value)
            #return xml_handler.get_data()
        
        else:
            return Response("HTTP/1.1 "+HttpStatus.NOT_FOUND.value, ContentType.PLAIN.value, HttpStatus.NOT_FOUND.value, len(HttpStatus.NOT_FOUND.value))
        
    except NotAcceptableException as exception:
        return Response("HTTP/1.1 "+exception.message, ContentType.PLAIN.value, exception.message, len(exception.message))
    except Exception as e:
        logging.error(e)
        raise e
    
def check_accept_header(request, needed_comtent_type):
    if "accept" in request.headers:
        if request.headers["accept"] and (needed_comtent_type not in request.headers["accept"] and "*/*" not in request.headers["accept"]):
            raise NotAcceptableException()
    