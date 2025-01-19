import socket
import logging
from threading import Thread

from entity.models import KeepAliveData, Response
import validator
from entity.exceptions import NotFoundException, MethodNotAllowedException, BadRequestException, UnsupportedMediaTypeException, NotAcceptableException, NotImplementedException, PayloadTooLargeException

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(filename)s - %(funcName)s - %(message)s")

HOST = "localhost"
HOST_IP = "127.0.0.1"
PORT = 8080
DEFAULT_TIMEOUT = 100 
DEFAULT_MAX_REQUESTS = 5

def handle_client(client_socket, client_address):
    logging.info(f"Neue Verbindung von {client_address}\n")
    client_socket.settimeout(DEFAULT_TIMEOUT)

    keep_alive_data = KeepAliveData(DEFAULT_TIMEOUT, DEFAULT_MAX_REQUESTS, 0)

    try:
        while keep_alive_data.request_count < keep_alive_data.max_requests:
            try:
                raw_request = client_socket.recv(4096).decode()
                if not raw_request:
                    logging.info(f"Keine Daten von {client_address}. Verbindung wird geschlossen.")
                    break
                logging.info(f"Anfrage von {client_address}:\n{raw_request.strip()}\n")

                try:
                    if len(raw_request) > 3000:
                        raise PayloadTooLargeException

                    request = validator.unpack_request(raw_request)
                    response = request.handler(request)

                    if "connection" in request.headers and "keep-alive" in request.headers["connection"]:
                        connection = "Keep-Alive\r\n"
                        connection += f"Keep-Alive: timeout={keep_alive_data.keep_alive_timeout}, max={keep_alive_data.max_requests}"
                        response.connection = connection
                    else: 
                        response.connection = "close"
                        keep_alive_data.max_requests = 1

                except BadRequestException as exception:
                    response = exception.response
                except UnsupportedMediaTypeException as exception:
                    response = exception.response
                except NotAcceptableException as exception:
                    response = exception.response
                except NotFoundException as exception:
                    logging.info("not found exception")
                    response = exception.response
                except MethodNotAllowedException as exception:
                    response = exception.response
                except NotImplementedException as exception:
                    response = exception.response
                except PayloadTooLargeException as exception:
                    response = exception.response
                except Exception as e:
                    logging.error(e)
                    status = "500 Internal Server Error"
                    response = Response("HTTP/1.1 "+status, "text/plain", status, len(status))

                http_response = (
                    f"{response.status}\r\n"
                    f"Content-Type: {response.content_type}\r\n"
                    f"Content-Length: {response.content_length}\r\n"
                    f"Connection: {response.connection}\r\n"
                    "\r\n"
                    f"{response.body}"
                )
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
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST_IP, PORT))
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
            server_thread.join(1)  # Warten auf Strg + C
    except KeyboardInterrupt:
        logging.info("Strg + C erkannt. Server wird beendet...")
        server_running = False  # Setze Flag auf False, um den Server zu beenden
