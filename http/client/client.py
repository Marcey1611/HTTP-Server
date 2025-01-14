import socket
import argparse
import logging
import threading
import msvcrt
import time
import shlex

# Logging einrichten
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = "8080"


def send_request(client_socket, method, path, host, port, headers, body):
    """
    Sendet eine HTTP-Anfrage und gibt die Antwort zurück.
    """
    try:
        # Anfrage zusammenstellen
        request = f"{method} {path} HTTP/1.1\r\nHost: {host}:{port}\r\n"
        for key, value in headers.items():
            request += f"{key}: {value}\r\n"
        if body:
            request += f"Content-Length: {len(body)}\r\n"
        request += "\r\n"

        # Body hinzufügen (falls vorhanden)
        if body:
            request += body


        # Anfrage senden
        logging.info(f"Anfrage:\n{request}")
        client_socket.sendall(request.encode())

    except socket.error as e:
        logging.error(f"Fehler bei der Anfrage: {e}")
        return None


def initial_parse_args():
    parser = argparse.ArgumentParser(description="HTTP-Client mit Keep-Alive-Unterstützung")
    parser.add_argument("method", type=str, help="HTTP-Methode (z. B. GET)")
    parser.add_argument("path", type=str, help="Pfad der Ressource (z. B. /)")
    parser.add_argument("--host", type=str, required=True, help="Hostname oder IP-Adresse des Servers")
    parser.add_argument("--port", type=int, required=True, help="Port des Servers")
    parser.add_argument("--headers", nargs="+", help="Zusätzliche HTTP-Header im Format Key:Value")
    parser.add_argument("--body", type=str, help="Body der Anfrage als String")
    return parser.parse_args()

def process_command(command):
    """Parst und verarbeitet komplexe Befehle."""
    parser = argparse.ArgumentParser(description="Process client commands.")
    parser.add_argument("method", type=str, help="HTTP method (e.g., GET, POST, PUT, DELETE)")
    parser.add_argument("path", type=str, help="API endpoint (e.g., /json/add_user)")
    parser.add_argument("--headers", nargs="+", help="Headers as key-value pairs (e.g., 'User-Agent:CustomClient')")
    parser.add_argument("--body", type=str, help="JSON string for the request body")

    try:
        # Parse command
        args = parser.parse_args(shlex.split(command))

        # Body prüfen
        body = None
        if args.body:
            body = args.body

        # Ergebnis ausgeben
        print(f"Method: {args.method}")
        print(f"Path: {args.path}")
        print(f"Headers: {args.headers}")
        print(f"Body: {body}")
    except Exception as e:
        print(f"Fehler beim Verarbeiten des Befehls: {e}")
    return args

def convert_headers_to_dict(args):
    headers = {}
    if args.headers:
        for header in args.headers:
            if ":" in header:
                key, value = header.split(":", 1)
                headers[key.strip()] = value.strip()
    return headers


def create_connection(args):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((args.host, args.port))
        client_socket.setblocking(False)  # Nicht-Blockiermodus aktivieren
        logging.info(f"Verbindung zu {args.host}:{args.port} hergestellt.")
        return client_socket
    except socket.error as e:
        raise e


def input_thread_function(stop_event, client_socket):
    """
    Funktion für den Benutzereingabe-Thread.
    """
    host, port = client_socket.getpeername()
    user_input = ""
    while not stop_event.is_set():
        try:
            # Prüfen, ob eine Taste gedrückt wurde
            if msvcrt.kbhit():
                char = msvcrt.getwch()  # Einzelnes Zeichen lesen
                if char == "\r":  # Enter-Taste erkannt
                    print("")  # Neue Zeile in der Konsole
                    if user_input.lower() in ["exit", "quit"]:
                        logging.info("Beenden des Clients...")
                        stop_event.set()
                        break
                    try:
                        args = process_command(user_input)
                        headers = convert_headers_to_dict(args)

                        send_request(client_socket, args.method, args.path, host, port, headers, args.body)
                    except ValueError:
                        logging.error("Ungültige Eingabe! Beispiel: GET /")
                    user_input = ""  # Eingabe zurücksetzen
                elif char == "\b":  # Backspace-Taste erkannt
                    user_input = user_input[:-1]
                    print("\b \b", end="", flush=True)  # Zeichen löschen
                else:
                    user_input += char
                    print(char, end="", flush=True)  # Zeichen anzeigen
            time.sleep(0.1)  # Kurz warten, um CPU-Auslastung zu reduzieren
        except KeyboardInterrupt:
            logging.info("Abbruch durch Benutzer (Ctrl+C).")
            stop_event.set()
            break


def main():
    args = initial_parse_args()
    headers = convert_headers_to_dict(args)
    body = args.body
    logging.info(f"Body: {body}")

    client_socket = None  # Vorinitialisierung, um Fehler im finally-Block zu vermeiden
    try:
        client_socket = create_connection(args)
        send_request(client_socket, args.method, args.path, args.host, args.port, headers, body)

        # Stop-Ereignis für den Benutzereingabe-Thread
        stop_event = threading.Event()

        # Benutzereingabe-Thread starten
        input_thread = threading.Thread(target=input_thread_function, args=(stop_event, client_socket))
        input_thread.start()

        # Warten auf Server-Antwort oder Benutzerabbruch
        while not stop_event.is_set():
            try:
                # Antwort empfangen (Nicht-Blockierend)
                try:
                    response = client_socket.recv(4096).decode()
                    if response:
                        logging.info(f"Antwort:\n{response}")
                        logging.info("Gib eine neue Anfrage ein (z. B. GET /) oder 'exit' zum Beenden: ")
                    if not response:  # Verbindung wurde vom Server geschlossen
                        logging.info("Verbindung zum Server wurde geschlossen.")
                        stop_event.set()
                except BlockingIOError:
                    # Keine Daten verfügbar, kurz warten
                    time.sleep(0.1)

            except socket.error as e:
                logging.error(f"Fehler beim Warten auf Serverantwort: {e}")
                stop_event.set()
            except KeyboardInterrupt:
                logging.info("Abbruch durch Benutzer (Ctrl+C).")
                stop_event.set()

        # Warten, bis der Input-Thread beendet ist
        input_thread.join()

    except socket.error as e:
        logging.error(f"Socket-Fehler: {e}")
    except KeyboardInterrupt:
        logging.info("Abbruch durch Benutzer (Ctrl+C).")
    finally:
        if client_socket and client_socket.fileno() != -1:
            client_socket.close()
        logging.info("Verbindung geschlossen.")


if __name__ == "__main__":
    main()
