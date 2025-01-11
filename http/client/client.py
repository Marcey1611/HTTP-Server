import socket
import argparse
import logging
import re
import threading
import time

# Logging einrichten
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def parse_keep_alive_header(response):
    """
    Analysiert den Keep-Alive-Header in der Server-Antwort und gibt Timeout und max-Anfragen zurück.
    """
    timeout = None
    max_requests = None

    # Header Zeilen parsen
    headers = response.split("\r\n")
    for header in headers:
        if header.lower().startswith("keep-alive:"):
            match = re.search(r"timeout=(\d+)", header, re.IGNORECASE)
            if match:
                timeout = int(match.group(1))
            match = re.search(r"max=(\d+)", header, re.IGNORECASE)
            if match:
                max_requests = int(match.group(1))

    return timeout, max_requests


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

        # Antwort empfangen
        response = client_socket.recv(4096).decode()
        logging.info(f"Antwort:\n{response}")
        return response
    except socket.error as e:
        logging.error(f"Fehler bei der Anfrage: {e}")
        return None


def timeout_checker(timeout, stop_event):
    """
    Überwacht den Timeout und beendet den Client, wenn der Timeout überschritten wird.
    """
    time.sleep(timeout)
    if not stop_event.is_set():
        logging.warning("Timeout erreicht. Verbindung wird geschlossen.")
        stop_event.set()


def parse_args():
    parser = argparse.ArgumentParser(description="HTTP-Client mit Keep-Alive-Unterstützung")
    parser.add_argument("method", type=str, help="HTTP-Methode (z. B. GET)")
    parser.add_argument("path", type=str, help="Pfad der Ressource (z. B. /)")
    parser.add_argument("--host", type=str, required=True, help="Hostname oder IP-Adresse des Servers")
    parser.add_argument("--port", type=int, required=True, help="Port des Servers")
    parser.add_argument("--headers", nargs="+", help="Zusätzliche HTTP-Header im Format Key:Value")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout in Sekunden für Keep-Alive (Standard: 10 Sekunden)")
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
    client_socket.settimeout(args.timeout)
    client_socket.connect((args.host, args.port))
    logging.info(f"Verbindung zu {args.host}:{args.port} hergestellt.")
    return client_socket


def process_timeout_and_max_requests(timeout, max_requests, client_socket, stop_event):
    # Timeout und max_requests aus Keep-Alive-Header übernehmen
    if timeout:
        logging.info(f"Server-Timeout: {timeout} Sekunden")
        client_socket.settimeout(timeout)
    if max_requests:
        logging.info(f"Maximale Anfragen: {max_requests}")

    # Timeout-Überwachung starten
    timeout_thread = threading.Thread(target=timeout_checker, args=(timeout, stop_event))
    timeout_thread.daemon = True
    timeout_thread.start()


def input_thread_function(stop_event, request_count, max_requests, client_socket, args, headers):
    """
    Funktion für den Benutzereingabe-Thread.
    """
    while not stop_event.is_set():
        try:
            user_input = input("\nGib eine neue Anfrage ein (z. B. GET /) oder 'exit' zum Beenden: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                logging.info("Beenden des Clients...")
                stop_event.set()
                break

            # Anfragen parsen und senden
            method, path = user_input.split()
            response = send_request(client_socket, method, path, args.host, headers)
            request_count += 1

            # Überprüfen, ob max_requests erreicht ist
            if max_requests and request_count >= max_requests:
                logging.info("Maximale Anzahl von Anfragen erreicht. Beenden des Clients...")
                stop_event.set()

        except ValueError:
            logging.error("Ungültige Eingabe! Beispiel: GET /")
        except socket.timeout:
            logging.warning("Timeout erreicht. Verbindung wird geschlossen.")
            stop_event.set()


def main():
    args = parse_args()
    headers = convert_headers_to_dict(args)

    try:
        client_socket = create_connection(args)
        response = send_request(client_socket, args.method, args.path, args.host, headers)
        timeout, max_requests = parse_keep_alive_header(response)

        # Stop-Ereignis für den Timeout-Thread und den Benutzereingabe-Thread
        stop_event = threading.Event()

        # Timeout-Überwachung starten
        process_timeout_and_max_requests(timeout, max_requests, client_socket, stop_event)

        request_count = 1

        # Benutzereingabe-Thread starten
        input_thread = threading.Thread(target=input_thread_function, args=(stop_event, request_count, max_requests, client_socket, args, headers))
        input_thread.daemon = True
        input_thread.start()

        # Warten auf Timeout oder Benutzerabbruch
        while not stop_event.is_set():
            time.sleep(1)  # Warte in einer Schleife und überprüfe regelmäßig den Event-Status

        # Wenn der Timeout überschritten wurde oder der Benutzer 'exit' eingegeben hat, beende das Programm
        if stop_event.is_set():
            logging.info("Abbruch aufgrund von Timeout oder Benutzerabbruch.")

    except socket.error as e:
        logging.error(f"Socket-Fehler: {e}")
    finally:
        if client_socket.fileno() != -1:
            client_socket.close()
        logging.info("Verbindung geschlossen.")


if __name__ == "__main__":
    main()
