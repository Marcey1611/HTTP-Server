import socket
import logging
from threading import Thread

from entity.models import KeepAliveData, Response, Request
from entity.enums import HttpStatus, ContentType
import validator
from entity.exceptions import NotFoundException, MethodNotAllowedException, HTTPVersionNotSupportedException, BadRequestException, UnsupportedMediaTypeException, NotAcceptableException, NotImplementedException, PayloadTooLargeException, LengthRequiredException, UnprocessableEntityException, UnauthorizedException, ForbiddenException

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(filename)s - %(funcName)s - %(message)s")

HOST = "localhost"
HOST_IP = "127.0.0.1"
PORT = 8080
DEFAULT_TIMEOUT = 100 
DEFAULT_MAX_REQUESTS = 5

def handle_connection_header(headers, keep_alive_data, response: Response, connection_keep_alive):
    if headers is None:
        keep_alive_data.max_requests = 1
        return response, connection_keep_alive, keep_alive_data
    if "connection" not in headers and not connection_keep_alive:
        keep_alive_data.max_requests = 1
    elif "connection" in headers and "close" in headers["connection"]:
        response.headers["Connection"] = "close"
        keep_alive_data.max_requests = 1
    elif ("connection" in headers and "keep-alive" in headers["connection"]) or connection_keep_alive:
        response.headers["Connection"] = "keep-alive"
        response.headers["Keep-Alive"] = f"timeout={keep_alive_data.keep_alive_timeout}, max={keep_alive_data.max_requests}"
        connection_keep_alive = True
    else:
        response.body = "Invalid connection type."
        response.status = HttpStatus.BAD_REQUEST.value
        response.headers["Content-Type"] = "text/plain"
        keep_alive_data.max_requests = 1
    return response, connection_keep_alive, keep_alive_data

def handle_client(client_socket, client_address):
    connection_keep_alive = False
    logging.info(f"Neue Verbindung von {client_address}\n")
    client_socket.settimeout(DEFAULT_TIMEOUT)

    keep_alive_data = KeepAliveData(DEFAULT_TIMEOUT, DEFAULT_MAX_REQUESTS, 0)
    
    try:
        while keep_alive_data.request_count < keep_alive_data.max_requests:
            request = None
            try:
                raw_request = client_socket.recv(4096).decode()
                if not raw_request:
                    logging.info(f"Keine Daten von {client_address}. Verbindung wird geschlossen.")
                    break
                logging.info(f"Anfrage von {client_address}:\n{raw_request.strip()}\n")
                try:
                    headers = None
                    
                    path, method, headers, body, query  = validator.unpack_request(raw_request)
                    if len(raw_request) > 3000:
                        raise PayloadTooLargeException("Request too large.")
                    request = validator.validate_request(path, method, headers, body, query, HOST, HOST_IP, PORT)
                    response = request.handler(request)
                    response, connection_keep_alive, keep_alive_data = handle_connection_header(headers, keep_alive_data, response, connection_keep_alive)


                except (NotFoundException, 
                        MethodNotAllowedException, 
                        BadRequestException, 
                        UnsupportedMediaTypeException, 
                        NotAcceptableException, 
                        NotImplementedException, 
                        PayloadTooLargeException, 
                        LengthRequiredException, 
                        UnprocessableEntityException, 
                        UnauthorizedException, 
                        ForbiddenException,
                        HTTPVersionNotSupportedException) as exception:
                    response = exception.response
                    response, connection_keep_alive, keep_alive_data = handle_connection_header(headers, keep_alive_data, response, connection_keep_alive)

                except Exception as exception:
                    logging.error(exception)
                    headers = {}
                    headers['Content-Type'] = ContentType.PLAIN.value
                    response = Response(HttpStatus.INTERNAL_SERVER_ERROR.value, headers, HttpStatus.INTERNAL_SERVER_ERROR.value)
                    response, connection_keep_alive, keep_alive_data = handle_connection_header(headers, keep_alive_data, response, connection_keep_alive)


                #response, connection_keep_alive, keep_alive_data = handle_connection_header(headers, keep_alive_data, response, connection_keep_alive)

                http_response = response.build_http_response()

                client_socket.sendall(http_response.encode())
                logging.info(f"Antwort gesendet:\n{http_response.strip()}\n")

                keep_alive_data.request_count += 1
                logging.info(f"Anfrage {keep_alive_data.request_count}/{keep_alive_data.max_requests} verarbeitet.")

                client_socket.settimeout(keep_alive_data.keep_alive_timeout)

            except socket.timeout:
                logging.info(f"Timeout von {keep_alive_data.keep_alive_timeout} Sekunden erreicht. Verbindung wird geschlossen.")
                break

    except Exception as e:
        logging.error(f"Fehler bei der Verarbeitung von {client_address}: {e}")
    finally:
        client_socket.close()
        logging.info(f"Verbindung mit {client_address} geschlossen.")

def run_server():
    global server_running
    global HOST
    global PORT
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((HOST_IP, PORT))
    except OSError as e:
        server_socket.bind((HOST_IP, 0))
        PORT = server_socket.getsockname()[1]
    server_socket.listen(5)
    server_socket.settimeout(1.0)

    logging.info(f"Server läuft auf {HOST_IP}:{PORT}")

    try:
        while server_running:
            try:
                client_socket, client_address = server_socket.accept()
                thread = Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
                thread.start()
            except socket.timeout:
                continue
    except Exception as e:
        logging.error(f"Server-Fehler: {e}")
    finally:
        server_socket.close()
        logging.info("Server wurde heruntergefahren.")

if __name__ == "__main__":
    server_running = True
    server_thread = Thread(target=run_server)
    server_thread.start()

    try:
        while server_thread.is_alive():
            server_thread.join(1)
    except KeyboardInterrupt:
        logging.info("Strg + C erkannt. Server wird beendet...")
        server_running = False
