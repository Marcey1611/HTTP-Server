import socket
import argparse
import logging
import re
import threading
import time

# Logging einrichten
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

goon = False

def send_request(client_socket, method, path, host, headers):
    """
    Sendet eine HTTP-Anfrage und gibt die Antwort zurück.
    """
    try:
        # Anfrage zusammenstellen
        request = f"{method} {path} HTTP/1.1\r\nHost: {host}\r\n"
        for key, value in headers.items():
            request += f"{key}: {value}\r\n"
        request += "\r\n"

        # Anfrage senden
        logging.info(f"Anfrage:\n{request}")
        client_socket.sendall(request.encode())

    except socket.error as e:
        logging.error(f"Fehler bei der Anfrage: {e}")
        return None

def parse_args():
    parser = argparse.ArgumentParser(description="HTTP-Client mit Keep-Alive-Unterstützung")
    parser.add_argument("method", type=str, help="HTTP-Methode (z. B. GET)")
    parser.add_argument("path", type=str, help="Pfad der Ressource (z. B. /)")
    parser.add_argument("--host", type=str, required=True, help="Hostname oder IP-Adresse des Servers")
    parser.add_argument("--port", type=int, required=True, help="Port des Servers")
    parser.add_argument("--headers", nargs="+", help="Zusätzliche HTTP-Header im Format Key:Value")
    return parser.parse_args()


def convert_headers_to_dict(args):
    headers = {}
    if args.headers:
        for header in args.headers:
            if ":" in header:
                key, value = header.split(":", 1)
                headers[key.strip()] = value.strip()
    return headers


def create_connection(args):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((args.host, args.port))
    logging.info(f"Verbindung zu {args.host}:{args.port} hergestellt.")
    return client_socket


def input_thread_function(stop_event, client_socket, args, headers):
    """
    Funktion für den Benutzereingabe-Thread.
    """
    global goon

    while not stop_event.is_set():
        try:
            if goon:
                user_input = input("\nGib eine neue Anfrage ein (z. B. GET /) oder 'exit' zum Beenden: ").strip()
                goon = False
                if user_input.lower() in ["exit", "quit"]:
                    logging.info("Beenden des Clients...")
                    stop_event.set()
                    break

                # Anfragen parsen und senden
                method, path = user_input.split()
                
                send_request(client_socket, method, path, args.host, headers)
        except ValueError:
            logging.error("Ungültige Eingabe! Beispiel: GET /")
            continue


def main():
    global goon
    args = parse_args()
    headers = convert_headers_to_dict(args)

    try:
        client_socket = create_connection(args)
        response = send_request(client_socket, args.method, args.path, args.host, headers)

        # Stop-Ereignis für den Benutzereingabe-Thread
        stop_event = threading.Event()

        # Benutzereingabe-Thread starten
        input_thread = threading.Thread(target=input_thread_function, args=(stop_event, client_socket, args, headers))
        input_thread.daemon = True
        input_thread.start()

        # Warten auf Server-Abbruch oder Benutzerabbruch
        while not stop_event.is_set():
            try:
                # Antwort empfangen
                response = client_socket.recv(4096).decode()
                if response:
                    logging.info(f"Antwort:\n{response}")

                goon = True
                if not response:  # Wenn keine Antwort mehr kommt, wurde die Verbindung vom Server geschlossen
                    logging.info("Verbindung zum Server wurde geschlossen.")
                    stop_event.set()
            except socket.error as e:
                logging.error(f"Fehler beim Warten auf Serverantwort: {e}")
                stop_event.set()
        logging.info("Abbruch aufgrund von Server-Trennung oder Benutzerabbruch.")

    except socket.error as e:
        logging.error(f"Socket-Fehler: {e}")
    finally:
        if client_socket.fileno() != -1:
            client_socket.close()
        logging.info("Verbindung geschlossen.")


if __name__ == "__main__":
    main()
