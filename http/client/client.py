import socket
import argparse
import logging
import threading
import time
import shlex
import select
import sys
import base64
import hashlib

# Logging einrichten
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# bei parser als default setzten?!?!?!
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = "8080"

def send_request(client_socket, method, path, host, port, headers, body):
    """
    Sendet eine HTTP-Anfrage und gibt die Antwort zurück.
    """
    try:
        # Anfrage zusammenstellen
        request = f"{method} {path} HTTP/1.1\r\n"
        for key, value in headers.items():
            request += f"{key}: {value}\r\n"
        if body and "Content-Length" not in headers:
            request += f"Content-Length: {len(body)}\r\n"
        if "Host" not in headers:
            request += f"Host: {host}:{port}\r\n"
        request += "\r\n"

        # Body hinzufügen (falls vorhanden)
        if body:
            request += body

        # Anfrage senden
        logging.info(f"Anfrage:\n{request}")
        client_socket.sendall(request.encode())

    except socket.error as e:
        logging.error(f"Fehler bei der Anfrage: {e}")
        raise e
    except Exception as e:
        logging.error(f"Fehler bei der Anfrage: {e}")
        raise e

def initial_parse_args():
    parser = argparse.ArgumentParser(description="HTTP-Client mit Keep-Alive-Unterstützung")
    parser.add_argument("method", type=str, help="HTTP-Methode (z. B. GET)")
    parser.add_argument("path", type=str, help="Pfad der Ressource (z. B. /)")
    parser.add_argument("--host", type=str, required=True, help="Hostname oder IP-Adresse des Servers")
    parser.add_argument("--port", type=int, required=True, help="Port des Servers")
    parser.add_argument("--headers", nargs="+", help="Zusätzliche HTTP-Header im Format Key:Value")
    parser.add_argument("--body", type=str, help="Body der Anfrage als String")
    
    try:
        return parser.parse_args()
    except SystemExit as e:
        if e.args[0] != 0:
            logging.error("Beim parsen der Argumente ist ein Fehler aufgetreten!")
            logging.error("Bitte erneut versuchen!")
            raise Exception
        raise e
    except Exception as e:
        logging.error(f"Fehler beim parsen der Argumente: {e}")
        raise e

def process_command(command):
    """Parst und verarbeitet komplexe Befehle."""
    parser = argparse.ArgumentParser(description="Process client commands.")
    parser.add_argument("method", type=str, help="HTTP method (e.g., GET, POST, PUT, DELETE)")
    parser.add_argument("path", type=str, help="API endpoint (e.g., /json/add_user)")
    parser.add_argument("--headers", nargs="+", help="Headers as key-value pairs (e.g., 'User-Agent:CustomClient')")
    parser.add_argument("--body", type=str, help="JSON string for the request body")

    try:
        return parser.parse_args(shlex.split(command))
    except SystemExit as e:
        if e.args[0]!= 0:
            logging.info(f"Beim parsen der Argumente ist ein Fehler aufgetreten!")
            raise Exception
        raise Exception
    except Exception as e:
        logging.error(f"Fehler beim parsen der Argumente: {e}")
        raise e

def convert_headers_to_dict(args):
    try:
        headers = {}
        if args.headers:
            for header in args.headers:
                if ":" in header:
                    key, value = header.split(":", 1)
                    key = key.strip()
                    value = value.strip()

                    # Spezielle Verarbeitung für den Authorization-Header
                    if key.lower() == "authorization" and value.lower().startswith("basic "):
                        # Extrahiere den Benutzernamen und das Passwort
                        credentials = value[6:].strip()  # Entferne "Basic "
                        
                        if ":" not in credentials:
                            raise ValueError("Authorization format should be 'username:password'")

                        username, password = credentials.split(":", 1)
                        
                        # Hashe das Passwort
                        hashed_password = hashlib.sha256(password.encode()).hexdigest()
                        
                        # Kombiniere Benutzername und gehashtes Passwort
                        new_credentials = f"{username}:{hashed_password}"
                        
                        # Kodierung in Base64
                        base64_credentials = base64.b64encode(new_credentials.encode()).decode("utf-8")
                        
                        # Aktualisiere den Authorization-Header
                        value = f"Basic {base64_credentials}"

                    headers[key] = value
        return headers
    except Exception as e:
        logging.error(f"Fehler beim Konvertieren der Header: {e}")
        raise e

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
    Funktion für den Benutzereingabe-Thread, der nicht blockiert.
    """
    host, port = client_socket.getpeername()
    while not stop_event.is_set():
        try:
            if select.select([sys.stdin], [], [], 0.5)[0]:  # Timeout von 0.5 Sekunden
                user_input = sys.stdin.readline().strip()  # Lesen der Eingabe
                if user_input:  # Wenn Eingabe vorhanden ist
                    try:
                        args = process_command(user_input)
                        headers = convert_headers_to_dict(args)
                        send_request(client_socket, args.method, args.path, host, port, headers, args.body)
                    except Exception:
                        logging.info("Gib eine neue Anfrage ein (z. B. GET /): ")

        except Exception as e:
            logging.error(f"Fehler im Eingabethread: {e}")
            stop_event.set()
            break
    logging.info("Eingabethread beendet.")

def main():
    try:
        args = initial_parse_args()
    except SystemExit:
        return
    except Exception as e:
        return
    
    headers = convert_headers_to_dict(args)
    body = args.body
    connection_keep_alive = False
    if "Connection" in headers and headers["Connection"] == "keep-alive":
        connection_keep_alive = True
    client_socket = None

    try:
        client_socket = create_connection(args)
        send_request(client_socket, args.method, args.path, args.host, args.port, headers, body)
        stop_event = threading.Event()
        if connection_keep_alive:
            input_thread = threading.Thread(target=input_thread_function, args=(stop_event, client_socket))
            input_thread.start()

        while not stop_event.is_set():
            try:
                try:
                    response = client_socket.recv(4096).decode()
                    if response:
                        logging.info(f"Antwort:\n{response}")
                        if connection_keep_alive:
                            logging.info("Gib eine neue Anfrage ein (z. B. GET /): ")
                    if not response:
                        logging.info("Verbindung zum Server wurde geschlossen.")
                        stop_event.set()
                except BlockingIOError:
                    time.sleep(0.1)

            except socket.error as e:
                logging.error(f"Fehler beim Warten auf Serverantwort: {e}")
                stop_event.set()
            except KeyboardInterrupt:
                logging.info("Abbruch durch Benutzer (Ctrl+C).")
                stop_event.set()
        if connection_keep_alive:
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
    try:
        main()
    except Exception as e:
        logging.error(f"Fehler im Hauptprogramm: {e}")