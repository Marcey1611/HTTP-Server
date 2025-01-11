import socket
import logging
from threading import Thread
import time

# Logging einrichten
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

HOST = "127.0.0.1"
PORT = 8080
TIMEOUT = 10  # Timeout für Client-Verbindungen in Sekunden

def handle_client(client_socket, client_address):
    logging.info(f"Neue Verbindung von {client_address}")
    client_socket.settimeout(TIMEOUT)  # Timeout für den Socket

    try:
        while True:
            try:
                # Empfange Anfrage vom Client
                request = client_socket.recv(4096).decode()
                current_time = time.time()

                # Wenn keine Anfrage empfangen wurde, Timeout überprüfen
                if not request:
                    if current_time - last_request_time > TIMEOUT:
                        logging.info(f"Timeout erreicht, keine Daten empfangen seit {TIMEOUT} Sekunden.")
                        break
                    else:
                        continue

                logging.info(f"Anfrage von {client_address}:\n{request.strip()}")

                # Zeitpunkt der letzten Anfrage speichern
                last_request_time = current_time

                # Prüfen, ob Connection: keep-alive gesetzt ist
                keep_alive = "keep-alive" in request.lower()

                # HTTP-Antwort erstellen
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n"
                    "Content-Length: 13\r\n"
                    "Connection: keep-alive\r\n\r\n"
                    "Hello, World!"
                )

                client_socket.sendall(response.encode())
                logging.info(f"Antwort gesendet:\n{response.strip()}")

                # Wenn Connection: keep-alive nicht gesetzt ist, beende die Verbindung
                if not keep_alive:
                    break

            except socket.timeout:
                logging.info(f"Timeout erreicht, Verbindung mit {client_address} wird geschlossen.")
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
