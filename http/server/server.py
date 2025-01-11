import socket
import logging
from threading import Thread
import time

# Logging einrichten
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

HOST = "127.0.0.1"
PORT = 8080
DEFAULT_TIMEOUT = 10  # Standard-Timeout für Keep-Alive in Sekunden
DEFAULT_MAX_REQUESTS = 5  # Standardanzahl maximaler Anfragen pro Verbindung

def handle_client(client_socket, client_address):
    logging.info(f"Neue Verbindung von {client_address}")
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

                logging.info(f"Anfrage von {client_address}:\n{request.strip()}")

                # Header analysieren
                headers = request.split("\r\n")
                for header in headers:
                    if header.lower().startswith("connection:"):
                        if "keep-alive" in header.lower():
                            logging.info("Client wünscht Keep-Alive.")
                        else:
                            logging.info("Client wünscht keine Keep-Alive-Verbindung.")
                            max_requests = 1  # Sofort beenden nach einer Anfrage
                    if header.lower().startswith("keep-alive:"):
                        try:
                            params = header.split(":")[1].strip().split(",")
                            for param in params:
                                key, value = param.split("=")
                                if key.strip().lower() == "timeout":
                                    keep_alive_timeout = int(value.strip())
                                if key.strip().lower() == "max":
                                    max_requests = int(value.strip())
                        except ValueError:
                            logging.warning("Fehlerhafte Keep-Alive-Header. Verwende Standardwerte.")

                # Antwort erstellen
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n"
                    f"Content-Length: 13\r\n"
                    f"Connection: keep-alive\r\n"
                    f"Keep-Alive: timeout={keep_alive_timeout}, max={max_requests}\r\n"
                    "\r\n"
                    "Hello, World!"
                )
                client_socket.sendall(response.encode())
                logging.info(f"Antwort gesendet:\n{response.strip()}")

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
