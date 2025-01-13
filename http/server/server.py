import socket
import logging
from threading import Thread
import json

from methods.get import get_handler
from methods.post import post_handler

# Logging einrichten
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

HOST = "127.0.0.1"
PORT = 8080
DEFAULT_TIMEOUT = 100  # Standard-Timeout für Keep-Alive in Sekunden
DEFAULT_MAX_REQUESTS = 5  # Standardanzahl maximaler Anfragen pro Verbindung

def parse_headers(request):
    """Extrahiert die Header aus der Anfrage und gibt sie als Dictionary zurück."""
    headers = {}
    lines = request.split("\r\n")
    for line in lines[1:]:  # Die erste Zeile ist die Anfrage-Methode (nicht benötigt für Header)
        if line == "":
            continue
        key, value = line.split(":", 1)
        headers[key.strip().lower()] = value.strip()
    return headers

def handle_client(client_socket, client_address):
    logging.info(f"Neue Verbindung von {client_address}\n")
    client_socket.settimeout(DEFAULT_TIMEOUT)  # Setzt Standard-Timeout

    # Initiale Werte für Keep-Alive-Parameter
    keep_alive_timeout = DEFAULT_TIMEOUT
    max_requests = DEFAULT_MAX_REQUESTS
    request_count = 0

    try:
        while request_count < max_requests:
            try:
                # Empfang der Anfrage
                request = client_socket.recv(4096).decode()
                if not request:  # Wenn keine Anfrage empfangen wurde
                    logging.info(f"Keine Daten von {client_address}. Verbindung wird geschlossen.")
                    break

                logging.info(f"Anfrage von {client_address}:\n{request.strip()}\n")

                method, path, _ = request.split(" ")[0], request.split(" ")[1], request.split(" ")[2]

                # Header als Dictionary extrahieren
                headers = parse_headers(request)

                if "connection" in headers and "keep-alive" in headers["connection"]:
                    connection = "Keep-Alive\r\n"
                    connection += f"Keep-Alive: timeout={keep_alive_timeout}, max={max_requests}"

                try:
                    # Methode und Pfad verarbeiten
                    if method == "GET":
                        status, content_type, body, content_length = get_handler.handle_get(path)
                    elif method == "POST":
                        if "content-type" not in headers:
                            status = "HTTP/1.1 400 Bad Request"
                            content_type = "text/plain"
                            body = "400 Bad Request"
                            content_length = len(body)
                        else:
                            # Extrahiere den Body (alles nach dem Header)
                            body = request.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in request else ""
                            logging.info(f"Body: {body}")

                            # Verarbeite den POST-Request
                            status, content_type, body, content_length = post_handler.handle_post(path, body, headers["content-type"])
                    else:
                        status = "HTTP/1.1 405 Method Not Allowed"
                        content_type = "text/plain"
                        body = "405 Method Not Allowed"
                        content_length = len(body)
                except Exception as e:
                    logging.error(e)
                    status = "HTTP/1.1 500 Internal Server Error"
                    content_type = "text/plain"
                    body = "500 Internal Server Error"
                    content_length = len(body)

                # Antwort erstellen
                response = (
                    f"{status}\r\n"
                    f"Content-Type: {content_type}\r\n"
                    f"Content-Length: {content_length}\r\n"
                    f"Connection: {connection}\r\n"
                    "\r\n"
                    f"{body}"
                )
                client_socket.sendall(response.encode())
                logging.info(f"Antwort gesendet:\n{response.strip()}\n")

                # Anzahl der Anfragen erhöhen
                request_count += 1
                logging.info(f"Anfrage {request_count}/{max_requests} verarbeitet.")

                # Timeout verlängern
                client_socket.settimeout(keep_alive_timeout)

            except socket.timeout:
                logging.info(f"Timeout von {keep_alive_timeout} Sekunden erreicht. Verbindung wird geschlossen.")
                break

    except Exception as e:
        logging.error(f"Fehler bei der Verarbeitung von {client_address}: {e}")
    finally:
        client_socket.close()
        logging.info(f"Verbindung mit {client_address} geschlossen.")

def run_server():
    global server_running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    server_socket.settimeout(1.0)  # Timeout für accept(), um KeyboardInterrupt zu erkennen

    logging.info(f"Server läuft auf {HOST}:{PORT}")

    try:
        while server_running:
            try:
                client_socket, client_address = server_socket.accept()
                thread = Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
                thread.start()
            except socket.timeout:
                continue  # Timeout ignorieren, weiter prüfen
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
